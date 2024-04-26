"""
 Author: Matt Hanson
 Created: 14/08/2020 11:04 AM
 """
from komanawa.basgra_nz_py.basgra_python import run_basgra_nz, _trans_manual_harv, get_month_day_to_nonleap_doy
from komanawa.basgra_nz_py.input_output_keys import matrix_weather_keys_pet
from support_for_tests import *
import inspect

from komanawa.basgra_nz_py.supporting_functions.plotting import \
    plot_multiple_results  # used in test development and debugging

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
    'irrig_dem_store',  # irrigation demand from storage (mm)
    'irrig_store',  # irrigation applied from storage (mm)
    'irrig_scheme',  # irrigation applied from the scheme (mm)
    'h2o_store_vol',  # volume of water in storage (m3)
    'h2o_store_per_area',  # h2o storage per irrigated area (mm)
    'IRR_TRIG_store',
    # irrigation trigger for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
    'IRR_TARG_store',
    # irrigation target for storage (fraction paw/FC), input, only relevant if calc_ind_store_demand
    'store_runoff_in',  # storage budget in from runoff or external model (m3)
    'store_leak_out',  # storage budget out from leakage (m3)
    'store_irr_loss',  # storage budget out from losses incurred with irrigation (m3)
    'store_evap_out',  # storage budget out from evaporation (NOTIMPLEMENTED) (m3)
    'store_scheme_in',  # storage budget in from the irrigation scheme (m3)
    'store_scheme_in_loss',  # storage budget out losses from the scheme to the storage basin (m3)
    'external_inflow',
    'store_overflow',

]

drop_internal = False  # shortcut make the droppable testing established tests change to True to drop new columns


def test_trans_manual_harv(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)
    params, matrix_weather, days_harvest, doy_irr = establish_org_input()

    days_harvest = clean_harvest(days_harvest, matrix_weather)
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
            'store_overflow', 'external_inflow'  # todo remove these when the tests are updated
        ]
        out2 = out.drop(columns=drop_keys_int, errors='ignore')
        correct_out2 = correct_out.drop(columns=drop_keys_int, errors='ignore')
    else:
        out2 = out.copy(True)
        correct_out2 = correct_out.copy(True)
    # check shapes
    assert out2.shape == correct_out2.shape, (
        f'something is wrong with the output shapes, '
        f'mismatched columns:{set(out2.keys()).symmetric_difference(correct_out2.keys())}')

    # check datatypes
    assert issubclass(out.values.dtype.type, float), 'outputs of the model should all be floats'

    out2 = out2.values
    out2[np.isnan(out2)] = -9999.99999
    correct_out3 = correct_out2.values
    correct_out3[np.isnan(correct_out2)] = -9999.99999
    # check values match for sample run
    isclose = np.isclose(out2, correct_out3)
    max_print = 20
    asmess = (f'{(~isclose).sum()} values do not match between the output and correct output '
              f'with rtol=1e-05, atol=1e-08'
              f'for columns: {correct_out2.columns[(~isclose).any(axis=0)]}\n' +
              f'{"correct": <16} | {"got": <16}\n' +
              '{}'.format("\n".join([f"{e: <16} | {f: <16}" for e, f in zip(correct_out3[~isclose],
                                                                            out2[~isclose])][0:max_print])))
    assert isclose.all(), asmess

    print('    model passed test\n')


def test_org_basgra_nz(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
    days_harvest = clean_harvest(days_harvest, matrix_weather)
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
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    # note this is linked to test_leap, so any inputs changes there should be mapped here
    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.5
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity

    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_trigger_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_irrigation_fraction(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .60  # irrigation of 60% of what is needed to get to field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_irrigation_fraction_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_water_short(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[matrix_weather.index > '2015-08-01', 'max_irr'] = 15
    matrix_weather.loc[:, 'irr_trig'] = 0.8
    matrix_weather.loc[:, 'irr_targ'] = 1

    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 91))

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_water_short_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_short_season(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_org_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather.loc[:, 'irr_trig'] = 1
    matrix_weather.loc[:, 'irr_targ'] = 1
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    doy_irr = list(range(305, 367)) + list(range(1, 61))

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_short_season_output.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_variable_irr_trig_targ(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

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

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, 'test_variable_irr_trig_targ.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_irr_paw(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
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

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    data_path = os.path.join(test_dir, '{}_data.csv'.format(test_nm))
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_pet_calculation(update_data=False):
    # keynote this test was not as well investigated as it was not needed for my work stream
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_peyman_input()
    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose,
                        supply_pet=False)

    data_path = os.path.join(test_dir, 'test_pet_calculation.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# Manual Harvest tests

def test_fixed_harvest_man(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
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

    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
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
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

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
    temp = pd.DataFrame(columns=days_harvest.keys(), dtype=float)
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

    dtyps = days_harvest.dtypes
    days_harvest = pd.concat((days_harvest, temp)).sort_values(['year', 'doy'])
    days_harvest = days_harvest.astype(dtyps)
    days_harvest.loc[:, 'year'] = days_harvest.loc[:, 'year'].astype(int)
    days_harvest.loc[:, 'doy'] = days_harvest.loc[:, 'doy'].astype(int)
    days_harvest = clean_harvest(days_harvest, matrix_weather)
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
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

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

    days_harvest = clean_harvest(days_harvest, matrix_weather)

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


def test_pass_soil_mosit(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = establish_org_input()
    params['irr_frm_paw'] = 1
    params['pass_soil_moist'] = 1

    per_data = pd.read_csv(os.path.join(test_dir, 'per_paw_fc.csv'))
    matrix_weather.loc[:, 'max_irr'] = per_data.loc[:, 'per_paw']
    # decrease soil moisture by 10% in Feb
    month = pd.to_datetime([f'{y}-{j:03d}' for y, j in matrix_weather.loc[:, ['year', 'doy']].itertuples(False, None)],
                           format='%Y-%j').month
    matrix_weather.loc[month == 2, 'max_irr'] *= 0.90
    matrix_weather.loc[month == 6, 'max_irr'] *= 0.80
    matrix_weather.loc[0, 'max_irr'] = 0.5

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'in_per_paw'] = matrix_weather.loc[:, 'max_irr'].values
    out.loc[:, 'per_paw'] = out.loc[:, 'PAW'] / out.loc[:, 'MXPAW']

    # test against my saved version (simply to have all columns
    data_path = os.path.join(test_dir, 'test_pass_soil_moist_paw.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    print('  testing percent fc')
    matrix_weather.loc[:, 'max_irr'] = per_data.loc[:, 'per_fc']
    # decrease soil moisture by 10% in Feb
    matrix_weather.loc[month == 2, 'max_irr'] *= 0.90
    matrix_weather.loc[month == 6, 'max_irr'] *= 0.80
    matrix_weather.loc[0, 'max_irr'] = 0.5
    params['irr_frm_paw'] = 0
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'in_per_fc'] = matrix_weather.loc[:, 'max_irr'].values
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']

    data_path = os.path.join(test_dir, 'test_pass_soil_moist_fc.csv')
    if update_data:
        out.to_csv(data_path)

    print('  testing against full dataset')
    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


# storage based tests

def test_full_refill(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 0
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 1000  # non-sensically high
    params['I_h2o_store_vol'] = 0.5
    params['runoff_area'] = 0
    params['runoff_frac'] = 0
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0
    params['stor_reserve_vol'] = 0
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # no use of storage
    matrix_weather.loc[:, 'irr_targ_store'] = 0
    matrix_weather.loc[:, 'external_inflow'] = 0

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_runoff_from_rain(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 1000  # non-sensically high
    params['I_h2o_store_vol'] = 0.5
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0
    params['stor_reserve_vol'] = 0
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # no use of storage
    matrix_weather.loc[:, 'irr_targ_store'] = 0
    matrix_weather.loc[:, 'external_inflow'] = 0

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_external_rainfall_runoff(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 0
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 1000  # non-sensically high
    params['I_h2o_store_vol'] = 0.5
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0
    params['stor_reserve_vol'] = 0
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # no use of storage
    matrix_weather.loc[:, 'irr_targ_store'] = 0
    matrix_weather.loc[:, 'external_inflow'] = 20
    specified_data = [
        20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]
    matrix_weather.loc[matrix_weather.index[:len(specified_data)], 'external_inflow'] = specified_data

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_leakage_prescribed_outflow(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 0
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 1000  # non-sensically high
    params['I_h2o_store_vol'] = 0.5
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0
    params['stor_reserve_vol'] = 0
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # no use of storage
    matrix_weather.loc[:, 'irr_targ_store'] = 0
    matrix_weather.loc[:, 'external_inflow'] = 20
    specified_data = [
        20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, -50, 20, 20, -25, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
        20,
        -10, -10, -10, -10, -10, -10, -10, -10, -20, -20, -20, -20, -20, -100,
    ]
    matrix_weather.loc[matrix_weather.index[:len(specified_data)], 'external_inflow'] = specified_data

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_store_irr_org_demand(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 0
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 15
    params['I_h2o_store_vol'] = 0.75
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0.1
    params['stor_reserve_vol'] = 2000

    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # not used for this test
    matrix_weather.loc[:, 'irr_targ_store'] = 0  # not used for this test
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    # re-run without storage
    params['use_storage'] = 0
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000

    data_path = os.path.join(test_dir, f'{test_nm}_no_store.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_store_irr_ind_demand(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 15
    params['I_h2o_store_vol'] = 0.75
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0.1
    params['stor_reserve_vol'] = 2000

    np.random.seed(1)
    matrix_weather.loc[:, 'max_irr'] = 5 + np.random.random_integers(-2, 5, len(matrix_weather))
    matrix_weather.loc[:, 'irr_trig_store'] = 0.80
    matrix_weather.loc[:, 'irr_targ_store'] = 0.90
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000
    out.loc[:, 'max_irr'] = matrix_weather.loc[:, 'max_irr']

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    np.random.seed(1)
    matrix_weather.loc[:, 'max_irr'] = 5 + np.random.random_integers(-5, 5, len(matrix_weather))
    matrix_weather.loc[:, 'irr_trig_store'] = 0.70
    matrix_weather.loc[:, 'irr_targ_store'] = 0.85
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000
    out.loc[:, 'max_irr'] = matrix_weather.loc[:, 'max_irr']

    data_path = os.path.join(test_dir, f'{test_nm}_2.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_store_irr_org_demand_paw(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['irr_frm_paw'] = 1
    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 0
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 15
    params['I_h2o_store_vol'] = 0.75
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0.1
    params['stor_reserve_vol'] = 2000

    matrix_weather.loc[:, 'max_irr'] = 5
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # not used for this test
    matrix_weather.loc[:, 'irr_targ_store'] = 0  # not used for this test
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_paw'] = out.loc[:, 'PAW'] / out.loc[:, 'MXPAW']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    # re-run without storage
    params['use_storage'] = 0
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000

    data_path = os.path.join(test_dir, f'{test_nm}_no_store.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_store_irr_ind_demand_paw(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['irr_frm_paw'] = 1
    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 1
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 15
    params['I_h2o_store_vol'] = 0.75
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1000  # no refill from scheme
    params['stor_refill_losses'] = 0
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0.1
    params['stor_reserve_vol'] = 2000

    np.random.seed(1)
    matrix_weather.loc[:, 'max_irr'] = 5 + np.random.random_integers(-2, 5, len(matrix_weather))
    matrix_weather.loc[:, 'irr_trig_store'] = 0.80
    matrix_weather.loc[:, 'irr_targ_store'] = 0.90
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_paw'] = out.loc[:, 'PAW'] / out.loc[:, 'MXPAW']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000
    out.loc[:, 'max_irr'] = matrix_weather.loc[:, 'max_irr']

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)

    np.random.seed(1)
    matrix_weather.loc[:, 'max_irr'] = 5 + np.random.random_integers(-5, 5, len(matrix_weather))
    matrix_weather.loc[:, 'irr_trig_store'] = 0.70
    matrix_weather.loc[:, 'irr_targ_store'] = 0.85
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_paw'] = out.loc[:, 'PAW'] / out.loc[:, 'MXPAW']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000
    out.loc[:, 'max_irr'] = matrix_weather.loc[:, 'max_irr']

    data_path = os.path.join(test_dir, f'{test_nm}_2.csv')
    if update_data:
        out.to_csv(data_path)

    correct_out = pd.read_csv(data_path, index_col=0)
    _output_checks(out, correct_out)


def test_store_refill_from_scheme(update_data=False):
    test_nm = inspect.currentframe().f_code.co_name
    print('testing: ' + test_nm)

    params, matrix_weather, days_harvest, doy_irr = get_input_for_storage_tests()

    params['runoff_from_rain'] = 1
    params['calc_ind_store_demand'] = 0
    params['stor_full_refil_doy'] = 240  # refill on day 240 each year
    params['abs_max_irr'] = 15
    params['I_h2o_store_vol'] = 0.75
    params['runoff_area'] = 10
    params['runoff_frac'] = 0.5
    params['stor_refill_min'] = 1  #
    params['stor_refill_losses'] = 0.2
    params['stor_leakage'] = 10  # slow leakage so fill is observable
    params['stor_irr_ineff'] = 0.1
    params['stor_reserve_vol'] = 2000

    np.random.seed(1)
    matrix_weather.loc[:, 'max_irr'] = np.random.choice([5, 15, 17], len(matrix_weather), p=[0.5, .25, .25])
    matrix_weather.loc[:, 'irr_trig_store'] = 1  # not used for this test
    matrix_weather.loc[:, 'irr_targ_store'] = 0  # not used for this test
    matrix_weather.loc[:, 'external_inflow'] = 0  # not used for this test

    days_harvest = clean_harvest(days_harvest, matrix_weather)
    matrix_weather = matrix_weather.loc[:, matrix_weather_keys_pet]
    out = run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=verbose)
    out.loc[:, 'per_fc'] = out.loc[:, 'WAL'] / out.loc[:, 'WAFC']
    out.loc[:, 'irrig_store_vol'] = out.loc[:, 'irrig_store'] / 1000 * params['irrigated_area'] * 10000
    out.loc[:, 'max_irr'] = matrix_weather.loc[:, 'max_irr']

    data_path = os.path.join(test_dir, f'{test_nm}.csv')
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
    # todo failing test test_reseed()

    # test 365 day calender run (no leap years)
    test_leap()

    # test passing soil moisture data in
    test_pass_soil_mosit()

    # input data for manual harvest check
    test_trans_manual_harv()

    # H2O storage tests
    test_full_refill()
    test_runoff_from_rain()
    test_external_rainfall_runoff()
    test_leakage_prescribed_outflow()
    test_store_irr_org_demand()
    test_store_irr_ind_demand()

    test_store_irr_org_demand_paw()
    test_store_irr_ind_demand_paw()
    # todo Problem!! test_store_refill_from_scheme()

    print('\n\nall established tests passed')
