"""
 Author: Matt Hanson
 Created: 21/08/2020 12:14 PM
 """

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_data')


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
    return outdata

def merge_data(outpath):
    woodward = get_woodward_weather()
    strs = ['{}-{:03d}'.format(e,f) for e,f in woodward[['year','doy']].itertuples(False, None)]
    woodward.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    niwa = get_lincoln_broadfield()
    strs = ['{}-{:03d}'.format(e,f) for e,f in niwa[['year','doy']].itertuples(False, None)]
    niwa.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    joined = pd.merge(woodward,niwa,suffixes=['_wood','_niwa'],on='date')
    joined.to_csv(outpath)

def plot_woodward_v_niwa():
    woodward = get_woodward_weather()
    strs = ['{}-{:03d}'.format(e,f) for e,f in woodward[['year','doy']].itertuples(False, None)]
    woodward.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    niwa = get_lincoln_broadfield()
    strs = ['{}-{:03d}'.format(e,f) for e,f in niwa[['year','doy']].itertuples(False, None)]
    niwa.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    joined = pd.merge(woodward,niwa,suffixes=['_wood','_niwa'],on='date')

    for k in woodward.keys():
        if k in ['year','doy','date']:
            continue
        fig,(ax) = plt.subplots()
        ax.scatter(woodward.date, woodward[k],c='r',label='wood')
        ax.scatter(niwa.date, niwa[k],c='b',label='niwa')
        ax.set_title(k)
        ax.legend()

        fig,(ax) = plt.subplots()
        ax.scatter(joined['{}_niwa'.format(k)],joined['{}_wood'.format(k)])
        ax.plot(joined['{}_niwa'.format(k)],joined['{}_niwa'.format(k)])
        ax.set_xlabel('niwa')
        ax.set_ylabel('woodward')
        ax.set_title(k)

    plt.show()


if __name__ == '__main__':
    merge_data(r"C:\matt_modelling_unbackedup\SLMACC_2020\niwa_woodward_data.csv")
    plot_woodward_v_niwa()
