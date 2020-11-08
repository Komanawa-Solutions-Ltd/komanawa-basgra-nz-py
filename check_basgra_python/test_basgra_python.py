"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
import os
import numpy as np
import pandas as pd
from basgra_python import run_basgra_nz
from input_output_keys import _matrix_weather_keys_pet, _matrix_weather_keys_peyman
from check_basgra_python.support_for_tests import establish_org_input, get_org_correct_values, get_lincoln_broadfield, \
    test_dir, establish_peyman_input

verbose = False


def _output_checks(out, correct_out):
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


def test_org_basgra_nz():
    print('testing original basgra_nz')
    params, matrix_weather, days_harvest = establish_org_input()
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)
    out.drop(columns=['WAFC', 'IRR_TARG', 'IRR_TRIG',
                      'IRRIG_DEM'], inplace=True)  # drop a newly added parameter

    correct_out = get_org_correct_values()
    _output_checks(out, correct_out)


def test_irrigation_trigger():
    print('testing irrigation trigger')
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys_pet]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    correct_out = pd.read_csv(os.path.join(test_dir, 'test_irrigation_trigger_output.csv'), index_col=0)
    _output_checks(out, correct_out)


def test_irrigation_fraction():
    print('testing irrigation fraction')
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys_pet]

    params['IRRIGF'] = .60  # irrigation of 60% of what is needed to get to field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)
    correct_out = pd.read_csv(os.path.join(test_dir, 'test_irrigation_fraction_output.csv'), index_col=0)
    _output_checks(out, correct_out)


def test_water_short():
    print('testing water shortage')
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[matrix_weather.index > '2015-08-01', 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.8
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    correct_out = pd.read_csv(os.path.join(test_dir, 'test_water_short_output.csv'), index_col=0)
    _output_checks(out, correct_out)


def test_short_season():
    print('testing short season')
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 60  # finish at end of feb

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    correct_out = pd.read_csv(os.path.join(test_dir, 'test_short_season_output.csv'), index_col=0)
    _output_checks(out, correct_out)


def test_variable_irr_trig_targ():
    print('testing time variable irrigation triggers and targets')
    params, matrix_weather, days_harvest = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[matrix_weather.index > '2013-08-01', 'irr_trig'] = 0.7

    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather.loc[(matrix_weather.index < '2012-08-01'), 'irr_targ'] = 0.8
    matrix_weather.loc[(matrix_weather.index > '2015-08-01'), 'irr_targ'] = 0.8

    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys_pet]

    params['IRRIGF'] = 1
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 60  # finish at end of feb

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)
    correct_out = pd.read_csv(os.path.join(test_dir, 'test_variable_irr_trig_targ.csv'), index_col=0)
    _output_checks(out, correct_out)


def test_pet_calculation():
    # todo write a test for the peyman equation weather
    print('testing pet calculation')
    params, matrix_weather, days_harvest = establish_peyman_input()
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, dll_path='default', supply_pet=False)
    correct_out = pd.read_csv(os.path.join(test_dir, ''),
                              index_col=0)  # todo check against scott farm run, and then include here
    _output_checks(out, correct_out)


# todo write a description in the readme file


if __name__ == '__main__':
    test_pet_calculation()
    test_org_basgra_nz()
    test_irrigation_trigger()
    test_irrigation_fraction()
    test_water_short()
    test_short_season()
    test_variable_irr_trig_targ()

    print('\n\nall tests passed')
