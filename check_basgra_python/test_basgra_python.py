"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
import os
import numpy as np
import pandas as pd
from basgra_python import run_basgra_nz, _trans_manual_harv
from input_output_keys import _matrix_weather_keys_pet, _matrix_weather_keys_peyman
from check_basgra_python.support_for_tests import establish_org_input, get_org_correct_values, get_lincoln_broadfield, \
    test_dir, establish_peyman_input, _clean_harvest, base_auto_harvest_data, base_manual_harvest_data

from supporting_functions.plotting import plot_multiple_results  # todo dadb

verbose = False

drop_keys = [  # newly added keys that must be dropped initially to manage tests, datasets are subsequently re-created
    'WAFC',
    'IRR_TARG',
    'IRR_TRIG',
    'IRRIG_DEM',
    'RYE_YIELD',
    'WEED_YIELD',
    'DM_RYE_RM',
    'DM_WEED_RM',
    'DMH_RYE',
    'DMH_WEED',
    'DMH',
]

view_keys = [
    'WAL',
    'WCL',
    'DM',
    'YIELD',
    'BASAL',
    'ROOTD',
    'IRRIG_DEM',
    'HARVFR',
    'RYE_YIELD',
    'WEED_YIELD',
    'DM_RYE_RM',
    'DM_WEED_RM',
    'DMH_RYE',
    'DMH_WEED',
    'DMH',
]


def test_trans_manual_harv(update_data=False):
    test_nm = 'test_trans_manual_harv'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest = establish_org_input()

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    np.random.seed(1)
    days_harvest.loc[:, 'harv_trig'] = np.random.rand(len(days_harvest))

    np.random.seed(2)
    days_harvest.loc[:, 'harv_targ'] = np.random.rand(len(days_harvest))

    np.random.seed(3)
    days_harvest.loc[:, 'weed_dm_frac'] = np.random.rand(len(days_harvest))

    out = _trans_manual_harv(days_harvest, matrix_weather)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def _output_checks(out, correct_out):
    # check shapes
    assert out.shape == correct_out.shape, 'something is wrong with the output shapes'

    # check datatypes
    assert issubclass(out.values.dtype.type, np.float), 'outputs of the model should all be floats'

    out = out.values
    correct_out = correct_out
    out[np.isnan(out)] = -9999.99999
    correct_out[np.isnan(correct_out)] = -9999.99999
    # check values match for sample run
    isclose = np.isclose(out, correct_out)
    asmess = '{} values do not match between the output and correct output with rtol=1e-05, atol=1e-08'.format(
        isclose.sum())
    assert isclose.all(), asmess

    print('    model passed test\n')


def test_org_basgra_nz(update_data=False):
    print('testing original basgra_nz')
    params, matrix_weather, days_harvest = establish_org_input()
    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    # test against my saved version (simply to have all columns #todo
    data_path = os.path.join(test_dir, 'test_org_basgra.csv')
    if update_data:
        out.to_csv(data_path)

    print('  testing against full dataset')
    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    # test to the original data provided by Simon Woodward

    out.drop(columns=drop_keys, inplace=True)  # remove all of the newly added keys

    print('  testing against Simon Woodwards original data')
    correct_out2 = get_org_correct_values()
    _output_checks(out, correct_out2)


def test_irrigation_trigger(update_data=False):
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

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_trigger_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_irrigation_fraction(update_data=False):
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

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_fraction_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_water_short(update_data=False):
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

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_water_short_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_short_season(update_data=False):
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

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_short_season_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_variable_irr_trig_targ(update_data=False):
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

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_variable_irr_trig_targ.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_pet_calculation(update_data=False):
    # note this test was not as throughrougly investigated as it was not needed for my work stream
    print('testing pet calculation')
    params, matrix_weather, days_harvest = establish_peyman_input()
    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, dll_path='default', supply_pet=False)

    data_path = os.path.join(test_dir, 'test_pet_calculation.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# Manual Harvest tests

def test_fixed_harvest_man(update_data=False):
    test_nm = 'test_fixed_harvest_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest = establish_org_input()
    params['fixed_removal'] = 1
    params['opt_harvfrin'] = 1

    days_harvest = base_manual_harvest_data()

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 2500
    days_harvest.loc[idx, 'harv_targ'] = 1000
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 1000
    days_harvest.loc[idx, 'harv_targ'] = 10
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2017-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 2000
    days_harvest.loc[idx, 'harv_targ'] = 100
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    days_harvest.drop(columns=['date'], inplace=True)

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_harv_trig_man(update_data=False):
    # test manaual harvesting dates with a set trigger, weed fraction set to zero
    test_nm = 'test_harv_trig_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest = establish_org_input()
    params['fixed_removal'] = 0
    params['opt_harvfrin'] = 1

    days_harvest = base_manual_harvest_data()

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.5
    days_harvest.loc[idx, 'harv_trig'] = 2500
    days_harvest.loc[idx, 'harv_targ'] = 2200
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 1000
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2017-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 1500
    days_harvest.loc[idx, 'harv_targ'] = 1000
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    days_harvest.drop(columns=['date'], inplace=True)

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)



def test_weed_fraction_man(update_data=False):
    # test manual harvesting trig set to zero +- target with weed fraction above 0
    test_nm = 'test_weed_fraction_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest = establish_org_input()
    params['fixed_removal'] = 0
    params['opt_harvfrin'] = 1

    days_harvest = base_manual_harvest_data()

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.5
    days_harvest.loc[idx, 'harv_trig'] = 2500
    days_harvest.loc[idx, 'harv_targ'] = 2200
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 1000
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0.5

    idx = days_harvest.date >= '2017-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 1500
    days_harvest.loc[idx, 'harv_targ'] = 1000
    days_harvest.loc[idx, 'weed_dm_frac'] = 1

    days_harvest.drop(columns=['date'], inplace=True)

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# automatic harvesting tests

def test_auto_harv_trig(update_data=False):
    test_nm = 'test_auto_harv_trig'
    print('testing: ' + test_nm)

    # test auto harvesting dates with a set trigger, weed fraction set to zero
    params, matrix_weather, days_harvest = establish_org_input()
    params['opt_harvfrin'] = 1

    days_harvest = base_auto_harvest_data(matrix_weather)

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 3000
    days_harvest.loc[idx, 'harv_targ'] = 2000
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.75
    days_harvest.loc[idx, 'harv_trig'] = 2500
    days_harvest.loc[idx, 'harv_targ'] = 1500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    days_harvest.drop(columns=['date'], inplace=True)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_auto_harv_fixed(update_data=False):
    test_nm = 'test_auto_harv_fixed'
    print('testing: ' + test_nm)

    # test auto harvesting dates with a set trigger, weed fraction set to zero
    params, matrix_weather, days_harvest = establish_org_input()
    days_harvest = base_auto_harvest_data(matrix_weather)
    params['fixed_removal'] = 1
    params['opt_harvfrin'] = 1

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 3000
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.75
    days_harvest.loc[idx, 'harv_trig'] = 1500
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0

    days_harvest.drop(columns=['date'], inplace=True)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_weed_fraction_auto(update_data=False):
    # test auto harvesting trig set +- target with weed fraction above 0

    test_nm = 'test_weed_fraction_auto'
    print('testing: ' + test_nm)

    # test auto harvesting dates with a set trigger, weed fraction set to zero
    params, matrix_weather, days_harvest = establish_org_input()
    params['opt_harvfrin'] = 1

    days_harvest = base_auto_harvest_data(matrix_weather)

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 3000
    days_harvest.loc[idx, 'harv_targ'] = 2000
    days_harvest.loc[idx, 'weed_dm_frac'] = 1.25

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.75
    days_harvest.loc[idx, 'harv_trig'] = 2500
    days_harvest.loc[idx, 'harv_targ'] = 1500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0.75

    days_harvest.drop(columns=['date'], inplace=True)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_weed_fixed_harv_auto(update_data=False):
    # test auto fixed harvesting trig set +- target with weed fraction above 0
    test_nm = 'test_weed_fixed_harv_auto'
    print('testing: ' + test_nm)

    # test auto harvesting dates with a set trigger, weed fraction set to zero
    params, matrix_weather, days_harvest = establish_org_input()
    days_harvest = base_auto_harvest_data(matrix_weather)
    params['fixed_removal'] = 1
    params['opt_harvfrin'] = 1

    idx = days_harvest.date < '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 1
    days_harvest.loc[idx, 'harv_trig'] = 3000
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 0.5

    idx = days_harvest.date >= '2014-01-01'
    days_harvest.loc[idx, 'frac_harv'] = 0.75
    days_harvest.loc[idx, 'harv_trig'] = 1500
    days_harvest.loc[idx, 'harv_targ'] = 500
    days_harvest.loc[idx, 'weed_dm_frac'] = 1

    days_harvest.drop(columns=['date'], inplace=True)
    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# todo write a description in the readme file


if __name__ == '__main__':



    test_org_basgra_nz()
    test_irrigation_trigger()
    test_irrigation_fraction()
    test_water_short()
    test_short_season()
    test_variable_irr_trig_targ()
    test_pet_calculation()

    test_trans_manual_harv()
    test_harv_trig_man()
    test_fixed_harvest_man()
    test_weed_fraction_auto()
    test_auto_harv_trig()
    test_weed_fixed_harv_auto()
    test_auto_harv_fixed()
    test_weed_fraction_man()
    print('\n\nall established tests passed')
