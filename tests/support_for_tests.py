"""
 Author: Matt Hanson
 Created: 27/08/2020 11:13 AM
 """
import pandas as pd
import os
import numpy as np
from komanawa.basgra_nz_py.supporting_functions.conversions import convert_RH_vpa
from komanawa.basgra_nz_py.supporting_functions.woodward_2020_params import get_woodward_mean_full_params
from copy import deepcopy

test_dir = os.path.join(os.path.dirname(__file__), 'test_data')


def establish_peyman_input(return_pet=False):
    # use the scott farm so that it doesn't need irrigation
    # time period [2010 - 2013)

    # load weather data
    weather_path = os.path.join(test_dir, 'hamilton_ruakura_ews2010-2013_{}.csv')

    pressure = pd.read_csv(os.path.join(test_dir, 'hamilton_AWS_pressure.csv'),
                           skiprows=8).loc[:, ['year',
                                               'doy',
                                               'pmsl']].set_index(['year', 'doy'])

    rain = pd.read_csv(weather_path.format('rain')).loc[:, ['year',
                                                            'doy',
                                                            'rain']].set_index(['year', 'doy'])

    temp = pd.read_csv(weather_path.format('temp')).loc[:, ['year',
                                                            'doy',
                                                            'tmax', 'tmin']].set_index(['year', 'doy'])

    rad = pd.read_csv(weather_path.format('rad')).loc[:, ['year',
                                                          'doy',
                                                          'radn']].set_index(['year', 'doy'])

    wind = pd.read_csv(weather_path.format('wind')).loc[:, ['year',
                                                            'doy',
                                                            'wind']].set_index(['year', 'doy'])

    pet = pd.read_csv(weather_path.format('pet')).loc[:, ['year',
                                                          'doy',
                                                          'pet']].set_index(['year', 'doy'])

    rh = pd.read_csv(weather_path.format('rh')).loc[:, ['year',
                                                        'doy',
                                                        'rh']]
    rh.loc[:, 'rh'] = pd.to_numeric(rh.rh, errors='coerce')
    rh = rh.groupby(['year', 'doy']).mean()

    dates = pd.Series(pd.date_range('2010-01-01', '2012-12-31'))
    matrix_weather = pd.DataFrame({'year': dates.dt.year,
                                   'doy': dates.dt.dayofyear,
                                   'to_delete': 1}).set_index(['year', 'doy'])

    matrix_weather = pd.merge(matrix_weather, temp, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, rain, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, rad, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, rh, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, wind, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, pet, how='outer', left_index=True, right_index=True)
    matrix_weather = pd.merge(matrix_weather, pressure, how='outer', left_index=True, right_index=True)
    matrix_weather.loc[:, 'vpa'] = convert_RH_vpa(matrix_weather.loc[:, 'rh'],
                                                  matrix_weather.loc[:, 'tmin'],
                                                  matrix_weather.loc[:, 'tmax'])

    matrix_weather = matrix_weather.fillna(method='ffill')
    if return_pet:
        matrix_weather.drop(columns=['rh', 'to_delete', 'wind', 'vpa', 'pmsl'], inplace=True)
    else:
        matrix_weather.drop(columns=['rh', 'to_delete', 'pet', 'pmsl'], inplace=True)
    matrix_weather.loc[:, 'max_irr'] = 10.
    matrix_weather.loc[:, 'irr_trig'] = 0
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather.loc[:, 'irr_trig_store'] = 0
    matrix_weather.loc[:, 'irr_targ_store'] = 1
    matrix_weather.loc[:, 'external_inflow'] = 0

    matrix_weather.reset_index(inplace=True)

    # load harvest data from Simon woodward's paper
    harvest_nm = 'harvest_Scott_0.txt'

    days_harvest = pd.read_csv(os.path.join(test_dir, harvest_nm),
                               delim_whitespace=True,
                               names=['year', 'doy', 'percent_harvest']
                               ).astype(int)  # floor matches what simon did.

    days_harvest = days_harvest.loc[(days_harvest.year >= 2010) & (days_harvest.year < 2013)]
    days_harvest.loc[:, 'frac_harv'] = days_harvest.loc[:, 'percent_harvest'] / 100
    days_harvest.loc[:, 'harv_trig'] = 0
    days_harvest.loc[:, 'harv_targ'] = 0
    days_harvest.loc[:, 'weed_dm_frac'] = 0

    days_harvest.loc[:, 'reseed_trig'] = -1
    days_harvest.loc[:, 'reseed_basal'] = 1

    days_harvest.drop(columns=['percent_harvest'], inplace=True)

    # load parameters from simon woodward's paper
    params = get_woodward_mean_full_params('scott')
    doy_irr = [0]
    return deepcopy(params), deepcopy(matrix_weather), deepcopy(days_harvest), deepcopy(doy_irr)


def _compair_pet():
    """just to compaire the pet and peyman results, the are slightly differnt,
    but I think that is due to different methods of calculating PET,"""
    from komanawa.basgra_nz_py.basgra_python import run_basgra_nz
    verbose = False
    params, matrix_weather, days_harvest, doy_irr = establish_peyman_input(False)
    peyman_out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, dll_path='default',
                               supply_pet=False)

    params, matrix_weather, days_harvest, doy_irr = establish_peyman_input(True)
    pet_out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, dll_path='default',
                            supply_pet=True)

    from komanawa.basgra_nz_py.supporting_functions.plotting import plot_multiple_results
    plot_multiple_results({'pet': pet_out, 'peyman': peyman_out})


def establish_org_input(site='scott'):
    if site == 'scott':
        harvest_nm = 'harvest_Scott_0.txt'
        weather_nm = 'weather_Scott.txt'
        # col = 1 + 8 * (1)
    elif site == 'lincoln':
        harvest_nm = 'harvest_Lincoln_0.txt'
        weather_nm = 'weather_Lincoln.txt'
        # col = 1 + 8 * (3 - 1)
    else:
        raise ValueError('unexpected site')
    params = get_woodward_mean_full_params(site)
    params = deepcopy(params)

    matrix_weather = pd.read_csv(os.path.join(test_dir, weather_nm),
                                 sep='\\s+', index_col=0,
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
    matrix_weather.loc[:, 'irr_trig'] = 0
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather.loc[:, 'irr_trig_store'] = 0
    matrix_weather.loc[:, 'irr_targ_store'] = 1
    matrix_weather.loc[:, 'external_inflow'] = 0

    days_harvest = pd.read_csv(os.path.join(test_dir, harvest_nm),
                               sep='\\s+',
                               names=['year', 'doy', 'percent_harvest']
                               ).astype(int)  # floor matches what simon did.

    days_harvest.loc[:, 'frac_harv'] = days_harvest.loc[:, 'percent_harvest'] / 100
    days_harvest.loc[:, 'harv_trig'] = 0.
    days_harvest.loc[:, 'harv_targ'] = 0.
    days_harvest.loc[:, 'weed_dm_frac'] = 0.
    days_harvest.loc[:, 'reseed_trig'] = -1.
    days_harvest.loc[:, 'reseed_basal'] = 1.

    days_harvest.drop(columns=['percent_harvest'], inplace=True)
    days_harvest = days_harvest.loc[days_harvest.year > 0]

    doy_irr = [0]
    return deepcopy(params), deepcopy(matrix_weather), deepcopy(days_harvest), deepcopy(doy_irr)


def clean_harvest(days_harvest, matrix_weather):
    days_harvest = deepcopy(days_harvest)
    stop_year = matrix_weather['year'].max()
    stop_day = matrix_weather.loc[matrix_weather.year == stop_year, 'doy'].max()
    days_harvest.loc[(days_harvest.year == stop_year) & (days_harvest.doy > stop_day),
    'year'] = -1  # cull harvest after end of weather data
    days_harvest = days_harvest.loc[days_harvest.year > 0]  # the size matching is handled internally

    return deepcopy(days_harvest)


def get_org_correct_values():
    sample_output_path = os.path.join(test_dir, 'sample_org_output.csv')
    sample_data = pd.read_csv(sample_output_path, index_col=0).astype(float)

    # add in new features of data
    sample_data.loc[:, 'IRRIG'] = 0  # new data, check
    return deepcopy(sample_data)


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
    strs = ['{}-{:03d}'.format(e, f) for e, f in matrix_weather[['year', 'doy']].itertuples(False, None)]
    matrix_weather.loc[:, 'date'] = pd.to_datetime(strs, format='%Y-%j')
    matrix_weather.set_index('date', inplace=True)
    matrix_weather = matrix_weather.loc[matrix_weather.index > '2011-08-01']
    matrix_weather.loc[:, 'max_irr'] = 10.
    matrix_weather.loc[:, 'irr_trig'] = 0
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather.loc[:, 'irr_trig_store'] = 0
    matrix_weather.loc[:, 'irr_targ_store'] = 1
    matrix_weather.loc[:, 'external_inflow'] = 0

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
    outdata.set_index(['year', 'doy'], inplace=True)

    for k, (start, stop) in line_breaks.items():
        temp = pd.read_csv(path, names=cols[k], skiprows=start - 1, nrows=stop - start + 1)
        temp.loc[:, 'year'] = temp.year.astype(int)
        temp.loc[:, 'doy'] = temp.doy.astype(int)
        temp.set_index(['year', 'doy'], inplace=True)
        tkeep = keep_cols[np.in1d(keep_cols, temp.keys())]
        for k2 in tkeep:
            outdata.loc[temp.index, k2] = temp.loc[:, k2]

    outdata = outdata.reset_index()
    for k in ['tmax', 'radn', 'pet']:
        outdata[k] = pd.to_numeric(outdata.loc[:, k], errors='coerce', downcast='float').astype(float)

    outdata.ffill(inplace=True)
    strs = ['{}-{:03d}'.format(e, f) for e, f in outdata[['year', 'doy']].itertuples(False, None)]
    outdata.loc[:, 'date'] = pd.to_datetime(strs, format='%Y-%j')
    outdata.set_index('date', inplace=True)
    outdata = outdata.loc[outdata.index > '2011-08-01']

    outdata.loc[:, 'max_irr'] = 10.
    outdata.loc[:, 'irr_trig'] = 0.
    outdata.loc[:, 'irr_targ'] = 1.
    outdata.loc[:, 'irr_trig_store'] = 0.
    outdata.loc[:, 'irr_targ_store'] = 1.
    outdata.loc[:, 'external_inflow'] = 0.

    return deepcopy(outdata)


def base_manual_harvest_data():
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    days_harvest.loc[:, 'frac_harv'] = 1
    days_harvest.loc[:, 'harv_trig'] = 3000
    days_harvest.loc[:, 'harv_targ'] = 1000
    days_harvest.loc[:, 'weed_dm_frac'] = 0
    days_harvest.loc[:, 'reseed_trig'] = -1
    days_harvest.loc[:, 'reseed_basal'] = 1

    strs = ['{}-{:03d}'.format(e, f) for e, f in days_harvest[['year', 'doy']].itertuples(False, None)]
    days_harvest.loc[:, 'date'] = pd.to_datetime(strs, format='%Y-%j')
    return deepcopy(days_harvest)


def base_auto_harvest_data(matrix_weather):
    strs = ['{}-{:03d}'.format(e, f) for e, f in matrix_weather[['year', 'doy']].itertuples(False, None)]

    days_harvest_out = pd.DataFrame({'year': matrix_weather.loc[:, 'year'],
                                     'doy': matrix_weather.loc[:, 'doy'],
                                     'frac_harv': np.zeros(len(matrix_weather)),  # set filler values
                                     'harv_trig': np.zeros(len(matrix_weather)) - 1,  # set flag to not harvest
                                     'harv_targ': np.zeros(len(matrix_weather)),  # set filler values
                                     'weed_dm_frac': np.zeros(len(matrix_weather)),  # set filler values
                                     'date': pd.to_datetime(strs, format='%Y-%j')
                                     })
    days_harvest_out.loc[:, 'reseed_trig'] = -1
    days_harvest_out.loc[:, 'reseed_basal'] = 1

    return deepcopy(days_harvest_out)


def get_input_for_storage_tests():
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[matrix_weather.index > '2015-08-01', 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.75
    matrix_weather.loc[:, 'irr_targ'] = 0.9

    params['IRRIGF'] = 1  # irrigation to 90% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))

    params['use_storage'] = 1
    params['irrigated_area'] = 10
    params['h2o_store_max_vol'] = 10000  # 100 mm storage
    params['h2o_store_SA'] = 0  # this is needed for evap, but not implemented currently

    # place holders, these need to be defined for each set
    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 0
    params['stor_full_refil_doy'] = 240
    params['abs_max_irr'] = 1000  # non-sensically high
    params['I_h2o_store_vol'] = 1
    params['runoff_area'] = 0
    params['runoff_frac'] = 0
    params['stor_refill_min'] = 0
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 0
    params['stor_irr_ineff'] = 0
    params['stor_reserve_vol'] = 0

    return deepcopy(params), deepcopy(matrix_weather), deepcopy(days_harvest), deepcopy(doy_irr)
