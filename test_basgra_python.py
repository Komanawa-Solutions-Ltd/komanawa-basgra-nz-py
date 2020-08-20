"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
import os
import numpy as np
import pandas as pd
from basgra_python import run_basgra_nz

test_dir = os.path.join(os.path.dirname(__file__), 'test_data')


def establish_input():
    params = pd.read_csv(os.path.join(test_dir, 'BASGRA_parModes.txt'),
                         delim_whitespace=True, index_col=0).iloc[:,
             1 + 8 * (1)]  # 99.9% sure this should fix the one index problem in R, check
    params = params.to_dict()

    matrix_weather = pd.read_csv(os.path.join(test_dir, 'weather_Scott.txt'),
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

    days_harvest = pd.read_csv(os.path.join(test_dir, 'harvest_Scott_0.txt'),
                               delim_whitespace=True,
                               names=['year', 'doy', 'percent_harvest']
                               ).astype(int)  # floor matches what simon did.

    days_harvest = days_harvest.loc[days_harvest.year > 0]  # the size matching is handled internally

    ndays = matrix_weather.shape[0]
    return params, matrix_weather, days_harvest


def get_correct_values():
    sample_output_path = os.path.join(test_dir, 'sample_output.csv')
    sample_data = pd.read_csv(sample_output_path, index_col=0).astype(float)
    return sample_data


def test_basgra_nz():
    params, matrix_weather, days_harvest = establish_input()
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)

    correct_out = get_correct_values()

    # check shapes
    assert out.shape == correct_out.shape, 'something is wrong with the output shapes'

    # check datatypes
    assert issubclass(out.values.dtype.type, np.float), 'outputs of the model should all be floats'

    # check values match for sample run
    isclose = np.isclose(out.values, correct_out.values)
    asmess = '{} values do not match between the output and correct output with rtol=1e-05, atol=1e-08'.format(
        isclose.sum())
    assert isclose.all(), asmess

    print('model passed tests')


if __name__ == '__main__':
    test_basgra_nz()
