"""
 Author: Matt Hanson
 Created: 27/08/2020 11:13 AM
 """
import pandas as pd
import os
import numpy as np

test_dir = os.path.join(os.path.dirname(__file__), 'test_data')


def establish_org_input(site='scott'):
    if site == 'scott':
        harvest_nm= 'harvest_Scott_0.txt'
        weather_nm='weather_Scott.txt'
        col=  1 + 8 * (1)
    elif site == 'lincoln':
        harvest_nm='harvest_Lincoln_0.txt'
        weather_nm='weather_Lincoln.txt'
        col=1 + 8*(3-1) # 99% sure this is lincoln
    else:
        raise ValueError('unexpected site')
    params = pd.read_csv(os.path.join(test_dir, 'BASGRA_parModes.txt'),
                         delim_whitespace=True, index_col=0).iloc[:, col]  # 99.9% sure this should fix the one index problem in R, check

    # add in my new values
    params.loc['IRRIGF'] = 0
    params.loc['doy_irr_start'] = 300
    params.loc['doy_irr_end'] = 90
    params.loc['irr_trig'] = 0

    params = params.to_dict()

    matrix_weather = pd.read_csv(os.path.join(test_dir, weather_nm),
                                 delim_whitespace=True, index_col=0,
                                 header=0,
                                 names=['year',
                                        'doy',
                                        'tmin',
                                        'tmax',
                                        'rain',
                                        'radn',
                                        'pet'])
    # set start date as doy 121 2011
    idx = (matrix_weather.year > 2011) | ((matrix_weather.year == 2011) & (matrix_weather.doy >= 121))
    matrix_weather = matrix_weather.loc[idx].reset_index(drop=True)
    # set end date as doy 120, 2017
    idx = (matrix_weather.year < 2017) | ((matrix_weather.year == 2017) & (matrix_weather.doy <= 120))
    matrix_weather = matrix_weather.loc[idx].reset_index(drop=True)

    matrix_weather.loc[:, 'max_irr'] = 10.

    days_harvest = pd.read_csv(os.path.join(test_dir, harvest_nm),
                               delim_whitespace=True,
                               names=['year', 'doy', 'percent_harvest']
                               ).astype(int)  # floor matches what simon did.

    days_harvest = days_harvest.loc[days_harvest.year > 0]  # the size matching is handled internally

    ndays = matrix_weather.shape[0]
    return params, matrix_weather, days_harvest


def get_org_correct_values():
    sample_output_path = os.path.join(test_dir, 'sample_org_output.csv')
    sample_data = pd.read_csv(sample_output_path, index_col=0).astype(float)

    # add in new features of data
    sample_data.loc[:,'IRRIG'] = 0 # new data, check
    return sample_data

def get_woodward_weather():
    matrix_weather = pd.read_csv(os.path.join(test_dir, 'weather_Lincoln.txt'),
                                 delim_whitespace=True, index_col=0,
                                 header=0,
                                 names=['year',
                                        'doy',
                                        'tmin',
                                        'tmax',
                                        'rain',
                                        'radn',
                                        'pet'])
    matrix_weather = matrix_weather.loc[matrix_weather.year >= 2010]
    matrix_weather = matrix_weather.loc[matrix_weather.year < 2018]
    strs = ['{}-{:03d}'.format(e,f) for e,f in matrix_weather[['year','doy']].itertuples(False, None)]
    matrix_weather.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    matrix_weather.set_index('date',inplace=True)
    matrix_weather = matrix_weather.loc[matrix_weather.index > '2011-08-01']
    return matrix_weather


def get_lincoln_broadfield():
    path = os.path.join(test_dir, 'Lincoln_Broadfield_Ews.csv')

    line_breaks = {
        'pet': [10, 2916],
        'rain': [2920, 5841],
        'tmaxmin': [5845, 8766],
        'rad': [8770, 11688],
    }

    cols = {
        'pet': ['station', 'year', 'doy', 'time', 'pet', 'per', 'type'],
        'rain': ['station', 'year', 'doy', 'time', 'rain', 'sog', 'rain_def', 'rain_runoff', 'per', 'freq'],
        'tmaxmin': ['station', 'year', 'doy', 'time', 'tmax', 'per1', 'tmin', 'per2',
                    'tgmin', 'per3', 'tmean', 'rhmean', 'per', 'freq'],
        'rad': ['station', 'year', 'doy', 'time', 'radn', 'per', 'type', 'freq'],
    }

    keep_cols = np.array(['pet', 'rain', 'rain_def', 'rain_runoff', 'tmax', 'tmin', 'radn'])

    temp = pd.date_range('01-01-2010', '31-12-2017', freq='D')
    year = temp.year.values
    doy = temp.dayofyear.values
    outdata = pd.DataFrame({'year': year, 'doy': doy}, )
    outdata.set_index(['year','doy'],inplace=True)

    for k, (start, stop) in line_breaks.items():
        temp = pd.read_csv(path, names=cols[k], skiprows=start - 1, nrows=stop - start+1)
        temp.loc[:,'year'] = temp.year.astype(int)
        temp.loc[:,'doy'] = temp.doy.astype(int)
        temp.set_index(['year','doy'],inplace=True)
        tkeep = keep_cols[np.in1d(keep_cols,temp.keys())]
        for k2 in tkeep:
            outdata.loc[temp.index,k2] = temp.loc[:,k2]

    outdata = outdata.reset_index()
    outdata.loc[:,'tmax'] = pd.to_numeric(outdata.loc[:,'tmax'],errors='coerce')
    outdata.fillna(method='ffill', inplace=True)
    strs = ['{}-{:03d}'.format(e,f) for e,f in outdata[['year','doy']].itertuples(False, None)]
    outdata.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    outdata.set_index('date',inplace=True)
    outdata = outdata.loc[outdata.index > '2011-08-01']

    return outdata

