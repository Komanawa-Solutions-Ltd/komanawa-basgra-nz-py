"""
 Author: Matt Hanson
 Created: 21/10/2020 10:53 AM
 """
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
from check_basgra_python.support_for_tests import get_lincoln_broadfield, get_woodward_weather
from basgra_python import run_basgra_nz
from check_basgra_python.support_for_tests import establish_org_input
from supporting_functions.plotting import plot_multiple_results


def run_old_basgra():
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_woodward_weather()
    time_idx = (matrix_weather.index >= np.datetime64('2012-06-01')) & (
            matrix_weather.index <= np.datetime64('2013-05-31'))
    matrix_weather = matrix_weather.loc[time_idx]
    matrix_weather.loc[:, 'max_irr'] = 10

    params['IRRIGF'] = 0  # no irrigation
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march
    params['irr_trig'] = 0  # never irrigate

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    return out


def run_frequent_harvest(freq, per):
    assert isinstance(per, int)
    assert isinstance(freq, int)
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    harv_range = pd.date_range('2012-06-01', '2013-05-30', freq='{}D'.format(freq))

    pers = list(np.repeat(per, len(harv_range)))
    pers.append(100)
    harv_range = pd.Series(harv_range).append(pd.Series(pd.date_range('2013-05-31', '2013-05-31'))).reset_index(
        drop=True)
    days_harvest = pd.DataFrame(index=range(len(harv_range)))
    days_harvest.loc[:, 'year'] = harv_range.dt.year
    days_harvest.loc[:, 'doy'] = harv_range.dt.dayofyear
    days_harvest.loc[:, 'percent_harvest'] = pers

    matrix_weather = get_woodward_weather()
    time_idx = (matrix_weather.index >= np.datetime64('2012-06-01')) & (
            matrix_weather.index <= np.datetime64('2013-05-31'))
    matrix_weather = matrix_weather.loc[time_idx]
    matrix_weather.loc[:, 'max_irr'] = 10

    params['IRRIGF'] = 0  # no irrigation
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march
    params['irr_trig'] = 0  # never irrigate

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    return out


if __name__ == '__main__':
    data = {
        '70_20d_harv': run_frequent_harvest(20, 90),
        '50_10d_harv': run_frequent_harvest(10, 50),
        '40_10d_harv': run_frequent_harvest(10, 40),
        '20_10d_harv': run_frequent_harvest(10, 20),
        '10_10d_harv': run_frequent_harvest(10, 10),
        'Woodward_model': run_old_basgra(),

    }
    plot_multiple_results(data, out_vars=['DM', 'YIELD', 'BASAL'],
                          outdir=r'M:\Shared drives\SLMACC_2020\pasture_growth_modelling\basgra_harvest_tuning\org_model')
