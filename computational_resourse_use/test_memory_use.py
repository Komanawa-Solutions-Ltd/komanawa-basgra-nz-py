"""
 a test for the memory usage, to use this script the memory profiler must be installed...
 https://pypi.org/project/memory-profiler/
$ pip install -U memory_profiler

 Author: Matt Hanson
 Created: 23/11/2020 9:50 AM
 """
from basgra_python import run_basgra_nz
from check_basgra_python.support_for_tests import establish_org_input, clean_harvest
import numpy as np
import pandas as pd
from memory_profiler import profile

@profile
def test():
    print(1)
    pass

@profile
def run_example_basgra():
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=False)

@profile
def support_for_memory_usage():
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
    start_year = matrix_weather['year'].min()
    start_day = matrix_weather.loc[matrix_weather.year == start_year, 'doy'].min()

    # set up a maximum run time
    idxs = np.random.random_integers(0, len(matrix_weather) - 1, 36600)
    matrix_weather = matrix_weather.iloc[idxs]
    expected_days = pd.Series(pd.date_range(start=pd.to_datetime('{}-{}'.format(start_year, start_day), format='%Y-%j'),
                                            periods=36600))
    matrix_weather.loc[:, 'year'] = expected_days.dt.year.values
    matrix_weather.loc[:, 'doy'] = expected_days.dt.dayofyear.values

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=False)


if __name__ == '__main__':
    test()
    run_example_basgra()
    support_for_memory_usage()
