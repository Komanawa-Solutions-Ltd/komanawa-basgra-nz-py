"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
import os
import numpy as np
import pandas as pd
from pasture_growth.basgra_nz.basgra_python import run_basgra_nz

test_dir = os.path.join(os.path.dirname(__file__), 'test_data')


def establish_input():
    params = pd.read_csv(os.path.join(test_dir, 'BASGRA_parModes.txt'),
                         delim_whitespace=True, index_col=0).iloc[:,
             1 + 8 * (1)]  # todo this should fix the one index problem in R, check
    params = params.to_dict()

    matrix_weather = None  # todo

    days_harvest = pd.read_csv(os.path.join(test_dir, 'harvest_Scott_0.txt'),
                               delim_whitespace=True, header=['year', 'doy', 'percent_harvest'])
    ndays = None  # todo
    raise NotImplementedError
    return params, matrix_weather, days_harvest, ndays


def get_correct_values(): #todo
    sample_output_path = os.path.join(test_dir, 'sample_output.csv')
    raise NotImplementedError


def test_basgra_nz():
    params, matrix_weather, days_harvest, ndays = establish_input()
    out = run_basgra_nz(params, matrix_weather, days_harvest, ndays)

    correct_out = get_correct_values()
    # todo assert out size
    # todo assert out datatypes
    # todo assert out values
