"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
import os
import numpy as np
import pandas as pd
from basgra_python import run_basgra_nz, _trans_manual_harv, get_month_day_to_nonleap_doy
from input_output_keys import matrix_weather_keys_pet
from check_basgra_python.support_for_tests import establish_org_input, get_org_correct_values, get_lincoln_broadfield, \
    test_dir, establish_peyman_input, _clean_harvest, base_auto_harvest_data, base_manual_harvest_data

from supporting_functions.plotting import plot_multiple_results  # used in test development and debugging

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
    'WAWP',
    'MXPAW',
    'PAW',
    'RESEEDED',

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
    'WAWP',  # # mm # Water in non-frozen root zone at wilting point
    'MXPAW',  # mm # maximum Profile available water
    'PAW',  # mm Profile available water at the time step

]


def test_trans_manual_harv(update_data=False):
    test_nm = 'test_trans_manual_harv'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()

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
    _output_checks(out, correct_out, dropable=False)


def _output_checks(out, correct_out, dropable=True):
    """
    base checker
    :param out: basgra data from current test
    :param correct_out: expected basgra data
    :param dropable: boolean, if True, can drop output keys, allows _output_checks to be used for not basgra data and
                     for new outputs to be dropped when comparing results.
    :return:
    """
    if dropable:
        # should normally be empty, but is here to allow easy checking of old tests against versions with a new output
        drop_keys_int = [

        ]
        out2 = out.drop(columns=drop_keys_int)
    else:
        out2 = out.copy(True)
    # check shapes
    assert out2.shape == correct_out.shape, 'something is wrong with the output shapes'

    # check datatypes
    assert issubclass(out.values.dtype.type, np.float), 'outputs of the model should all be floats'

    out2 = out2.values
    correct_out2 = correct_out.values
    out2[np.isnan(out2)] = -9999.99999
    correct_out2[np.isnan(correct_out2)] = -9999.99999
    # check values match for sample run
    isclose = np.isclose(out2, correct_out2)
    asmess = '{} values do not match between the output and correct output with rtol=1e-05, atol=1e-08'.format(
        (~isclose).sum())
    assert isclose.all(), asmess

    print('    model passed test\n')


def test_org_basgra_nz(update_data=False):
    print('testing original basgra_nz')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    # test against my saved version (simply to have all columns
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
    # note this is linked to test_leap, so any inputs changes there should be mapped here
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity

    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_trigger_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_irrigation_fraction(update_data=False):
    print('testing irrigation fraction')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .60  # irrigation of 60% of what is needed to get to field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_fraction_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_water_short(update_data=False):
    print('testing water shortage')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[matrix_weather.index > '2015-08-01', 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.8
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_water_short_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_short_season(update_data=False):
    print('testing short season')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 61))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_short_season_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_variable_irr_trig_targ(update_data=False):
    print('testing time variable irrigation triggers and targets')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[matrix_weather.index > '2013-08-01', 'irr_trig'] = 0.7

    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather.loc[(matrix_weather.index < '2012-08-01'), 'irr_targ'] = 0.8
    matrix_weather.loc[(matrix_weather.index > '2015-08-01'), 'irr_targ'] = 0.8

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = 1
    doy_irr = list(range(305, 367)) + list(range(1, 61))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_variable_irr_trig_targ.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_irr_paw(update_data=False):
    test_nm = 'test_irr_paw'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 0.9

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))
    params['irr_frm_paw'] = 1

    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_pet_calculation(update_data=False):
    # note this test was not as throughrougly investigated as it was not needed for my work stream
    print('testing pet calculation')
    params, matrix_weather, days_harvest, doy_irr = establish_peyman_input()
    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, dll_path='default',
                        supply_pet=False)

    data_path = os.path.join(test_dir, 'test_pet_calculation.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# Manual Harvest tests

def test_fixed_harvest_man(update_data=False):
    test_nm = 'test_fixed_harvest_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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

    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_harv_trig_man(update_data=False):
    # test manaual harvesting dates with a set trigger, weed fraction set to zero
    test_nm = 'test_harv_trig_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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

    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_weed_fraction_man(update_data=False):
    # test manual harvesting trig set to zero +- target with weed fraction above 0
    test_nm = 'test_weed_fraction_man'
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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

    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

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
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_auto_harv_fixed(update_data=False):
    test_nm = 'test_auto_harv_fixed'
    print('testing: ' + test_nm)

    # test auto harvesting dates with a set trigger, weed fraction set to zero
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, auto_harvest=True)

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
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, auto_harvest=True)

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
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
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
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, auto_harvest=True)

    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_reseed(update_data=False):
    print('testing reseeding')
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 1
    matrix_weather.loc[matrix_weather.index > '2015-08-01', 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    # these values are set to make observable changes in the results and are not reasonable values.
    params['reseed_harv_delay'] = 120
    params['reseed_LAI'] = 3
    params['reseed_TILG2'] = 10
    params['reseed_TILG1'] = 40
    params['reseed_TILV'] = 5000
    params['reseed_CLV'] = 100
    params['reseed_CRES'] = 25
    params['reseed_CST'] = 10
    params['reseed_CSTUB'] = 0.5

    doy_irr = list(range(305, 367)) + list(range(1, 91))
    temp = pd.DataFrame(columns=days_harvest.keys())
    for i, y in enumerate(days_harvest.year.unique()):
        if y == 2011:
            continue
        temp.loc[i, 'year'] = y
        temp.loc[i, 'doy'] = 152
        temp.loc[i, 'frac_harv'] = 0
        temp.loc[i, 'harv_trig'] = -1
        temp.loc[i, 'harv_targ'] = 0
        temp.loc[i, 'weed_dm_frac'] = 0
        temp.loc[i, 'reseed_trig'] = 0.75
        temp.loc[i, 'reseed_basal'] = 0.88
    days_harvest = pd.concat((days_harvest, temp)).sort_values(['year', 'doy'])
    days_harvest.loc[:, 'year'] = days_harvest.loc[:, 'year'].astype(int)
    days_harvest.loc[:, 'doy'] = days_harvest.loc[:, 'doy'].astype(int)
    days_harvest = _clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    to_plot = [  # used to check the test
        'RESEEDED',
        'PHEN',
        'BASAL',
        'YIELD',
        'DM_RYE_RM',
        'LAI',
        'TILG2',
        'TILG1',
        'TILV',
        'CLV',
        'CRES',
        'CST',
        'CSTUB',
    ]
    data_path = os.path.join(test_dir, 'test_reseed.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_leap(update_data=False):
    print('testing leap year')
    passed_test = []
    # note this is linked to test irrigation trigger, so any inputs changes there should be mapped here
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()  # this has a leap year in 2012 and 2016
    matrix_weather.loc[:, 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity

    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = _clean_harvest(days_harvest, matrix_weather)

    try:
        out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, run_365_calendar=True)
        passed_test.append(False)
    except AssertionError as val:
        passed_test.append(True)

    matrix_weather = matrix_weather.loc[~((matrix_weather.index.day == 29) & (matrix_weather.index.month == 2))]
    try:
        out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, run_365_calendar=True)
        passed_test.append(False)
    except AssertionError as val:
        passed_test.append(True)

    mapper = get_month_day_to_nonleap_doy()
    matrix_weather.loc[:, 'doy'] = [mapper[(m, d)] for m, d in
                                    zip(matrix_weather.index.month, matrix_weather.index.day)]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose, run_365_calendar=True)

    external_data_path = os.path.join(test_dir, 'test_irrigation_trigger_output.csv')
    # note this is linked to test irrigation trigger

    correct_out = pd.read_csv(external_data_path)
    correct_out.loc[:, 'date'] = pd.to_datetime(correct_out.loc[:, 'date'])
    correct_out.set_index('date', inplace=True)
    _output_checks(out.loc[out.index.year == 2011], correct_out.loc[correct_out.index.year == 2011])

    try:
        _output_checks(out, correct_out)
    except AssertionError:
        passed_test.append(True)

    # test doy and index.dayofyear do not match
    idx = ~(out.doy == out.index.dayofyear)

    # this should be off for all leap years as they have been shifted to a 365 calander
    assert set(out.loc[idx].index.year) == {2012, 2016}, 'should only be a mismatch for leap years'
    assert set(out.loc[idx].index.month) == {3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 'should only affect days after 2 month'
    assert idx.sum() == 612, 'there should only be 612 entries 2*(365-31-28)'

    assert all(passed_test), f'one of the checks within basgra did not work, check try associated with {passed_test}'

    data_path = os.path.join(test_dir, 'test_leap.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


if __name__ == '__main__':

    # input types tests
    test_org_basgra_nz()
    test_pet_calculation()

    # irrigation tests
    test_irrigation_trigger()
    test_irrigation_fraction()
    test_water_short()
    test_short_season()
    test_variable_irr_trig_targ()
    test_irr_paw()

    # harvest checks
    test_harv_trig_man()
    test_fixed_harvest_man()
    test_weed_fraction_auto()
    test_auto_harv_trig()
    test_weed_fixed_harv_auto()
    test_auto_harv_fixed()
    test_weed_fraction_man()

    # test reseed
    test_reseed()

    # test 365 day calender run (no leap years)
    test_leap()

    # input data for manual harvest check
    test_trans_manual_harv()

    print('\n\nall established tests passed')
