"""
This is a place to create a python wrapper for the BASGRA fortran model in fortarn_BASGRA_NZ

 Author: Matt Hanson
 Created: 12/08/2020 9:32 AM
 """
import numpy as np
import pandas as pd
from copy import deepcopy
from komanawa.basgra_nz_py.input_output_keys import param_keys, out_cols, days_harvest_keys, matrix_weather_keys_pet, \
    matrix_weather_keys_penman
from warnings import warn
from komanawa.basgra_nz_py.get_fortran_module import get_fortran_basgra

# this is the maximum number of weather days,
# it is hard coded into fortran_BASGRA_NZ/environment.f95 line 9
_max_weather_size = 36600


def run_basgra_nz(params, matrix_weather, days_harvest, doy_irr, verbose=False,
                  supply_pet=True, auto_harvest=False, run_365_calendar=False):
    """
    python wrapper for the fortran BASGRA code changes to the fortran code may require changes to this function runs the model for the period of the weather data

    :param params: dictionary, see input_output_keys.py, https://github.com/Komanawa-Solutions-Ltd/BASGRA_NZ_PY for more details
    :param matrix_weather: pandas dataframe of weather data, maximum entries set in _max_weather_size in line 24 of this file (currently 36600) see documentation for input columns at https://github.com/Komanawa-Solutions-Ltd/BASGRA_NZ_PY , note expected DOY will change depending on expect_no_leap_days
    :param days_harvest: days harvest dataframe must be same length as matrix_weather entries see documentation for input columns at https://github.com/Komanawa-Solutions-Ltd/BASGRA_NZ_PY , note expected DOY will change depending on expect_no_leap_days
    :param doy_irr: a list of the days of year to irrigate on, must be integers acceptable values: (0-366)
    :param verbose: boolean, if True the fortran function prints a number of statements for debugging purposes(depreciated)
    :param supply_pet: boolean, if True BASGRA expects pet to be supplied, if False the parameters required to calculate pet from the peyman equation are expected, the version must match the DLL if dll_path != 'default'
    :param auto_harvest: boolean, if True then assumes data is formated correctly for auto harvesting, if False, then assumes data is formatted for manual harvesting (e.g. previous version) and re-formats internally
    :param run_365_calendar: boolean, if True then run on a 365 day calender This expects that all leap days will be removed from matrix_weather and days_harvest. DOY is expected to be between 1 and 365.  This means that datetime objects defined by year and doy will be incorrect. instead use get_month_day_to_nonleap_doy to map DOY to datetime via month and day. This is how the index of the returned datetime will be passed.  For example for date 2024-03-01 (2024 is a leap year) the dayofyear via a datetime object will be 61, but if expect_no_leap_days=True basgra expects day of year to be 60. the index of the results will be a datetime object of equivalent to 2024-03-01, so  the output doy will not match the index doy and there will be no value on 2020-02-29. default False
    :return: pd.DataFrame(index=datetime index, columns = out_cols)
    """

    assert isinstance(supply_pet, bool), 'supply_pet param must be boolean'
    assert isinstance(auto_harvest, bool), 'auto_harvest param must be boolean'
    assert isinstance(run_365_calendar, bool), 'expect_no_leap_days must be boolean'

    # define DLL library path
    fortran_basgra = get_fortran_basgra(supply_pet)

    # define expected weather keys
    if supply_pet:
        _matrix_weather_keys = matrix_weather_keys_pet
    else:
        _matrix_weather_keys = matrix_weather_keys_penman

    doy_irr = np.atleast_1d(doy_irr)
    # test the input variables
    _test_basgra_inputs(params, matrix_weather, days_harvest, verbose, _matrix_weather_keys,
                        auto_harvest, doy_irr, run_365_calendar=run_365_calendar)

    nout = len(out_cols)
    ndays = len(matrix_weather)
    nirr = len(doy_irr)

    # define output indexes before data manipulation
    out_index = matrix_weather.index

    # copy everything and ensure order is correct
    params = deepcopy(params)
    matrix_weather = deepcopy(matrix_weather.loc[:, _matrix_weather_keys])
    days_harvest = deepcopy(days_harvest.loc[:, days_harvest_keys])

    # translate manual harvest inputs into fortran format
    if not auto_harvest:
        days_harvest = _trans_manual_harv(days_harvest, matrix_weather)

    # get variables into right python types
    params = np.array([params[e] for e in param_keys]).astype(float)
    matrix_weather = matrix_weather.values.astype(float)
    days_harvest = days_harvest.values.astype(float)
    doy_irr = doy_irr.astype(np.int32)

    # manage weather size,
    weather_size = len(matrix_weather)
    if weather_size < _max_weather_size:
        temp = np.zeros((_max_weather_size - weather_size, matrix_weather.shape[1]), float)
        matrix_weather = np.concatenate((matrix_weather, temp), 0)
    elif weather_size > _max_weather_size:
        raise ValueError(f'weather data is too long, maximum is {_max_weather_size} days, '
                         f'though this value can be modified in the fortran code: '
                         f'fortran_BASGRA_NZ/environment.f95 line 9 and {__file__} line 29')

    y = np.asfortranarray(np.zeros((ndays, nout), float))  # cannot set these to nan's or it breaks fortran

    y = fortran_basgra.basgra(params,
                              np.asfortranarray(matrix_weather),
                              days_harvest,
                              ndays,
                              nout,
                              nirr,
                              doy_irr,
                              verbose,
                              y=deepcopy(y))
    out = pd.DataFrame(y, out_index, out_cols)
    if run_365_calendar:
        mapper = get_month_day_to_nonleap_doy(key_doy=True)
        strs = [f'{y}-{mapper[doy][0]:02d}-{mapper[doy][1]:02d}' for y, doy in zip(out.year.values.astype(int),
                                                                                   out.doy.values.astype(int))]
        out.loc[:, 'date'] = pd.to_datetime(strs)
    else:
        strs = ['{}-{:03d}'.format(int(e), int(f)) for e, f in out[['year', 'doy']].itertuples(False, None)]
        out.loc[:, 'date'] = pd.to_datetime(strs, format='%Y-%j')

    out.set_index('date', inplace=True)

    return out


def _trans_manual_harv(days_harvest, matrix_weather):
    """
    translates manual harvest data to the format expected by fortran, check the details of the data in here.

    :param days_harvest: manual harvest data
    :param matrix_weather: weather data, mostly to get the right size
    :return: days_harvest (correct format for fortran code)
    """
    days_harvest = days_harvest.set_index(['year', 'doy'])
    days_harvest_out = pd.DataFrame({'year': matrix_weather.loc[:, 'year'],
                                     'doy': matrix_weather.loc[:, 'doy'],
                                     'frac_harv': np.zeros(len(matrix_weather)),  # set filler values
                                     'harv_trig': np.zeros(len(matrix_weather)) - 1,  # set flag to not harvest
                                     'harv_targ': np.zeros(len(matrix_weather)),  # set filler values
                                     'weed_dm_frac': np.zeros(len(matrix_weather)) * np.nan,  # set nas, filled later
                                     'reseed_trig': np.zeros(len(matrix_weather)) - 1,  # set flag to not reseed
                                     'reseed_basal': np.zeros(len(matrix_weather)),  # set filler values
                                     })
    days_harvest_out = days_harvest_out.set_index(['year', 'doy'])
    for k in set(days_harvest_keys) - {'year', 'doy'}:
        days_harvest_out.loc[days_harvest.index, k] = days_harvest.loc[:, k]

    days_harvest_out = days_harvest_out.reset_index()

    # fill the weed fraction so that DMH_WEED is always calculated

    if pd.isna(days_harvest_out.weed_dm_frac).iloc[0]:
        warn('weed_dm_frac is na for the first day of simulation, setting to first valid weed_dm_frac\n'
             'this does not affect the harvesting only the calculation of the DMH_weed variable.')

        idx = np.where(pd.notna(days_harvest_out.weed_dm_frac))[0][0]  # get first non-nan value
        id_val = pd.Series(days_harvest_out.index).iloc[0]
        days_harvest_out.loc[id_val, 'weed_dm_frac'] = days_harvest_out.loc[:, 'weed_dm_frac'].iloc[idx]

    days_harvest_out.loc[:, 'weed_dm_frac'] = days_harvest_out.loc[:, 'weed_dm_frac'].ffill()

    return days_harvest_out


def _test_basgra_inputs(params, matrix_weather, days_harvest, verbose, _matrix_weather_keys,
                        auto_harvest, doy_irr, run_365_calendar):
    # check parameters
    assert isinstance(verbose, bool), 'verbose must be boolean'
    assert isinstance(params, dict)
    assert set(params.keys()) == set(param_keys), 'incorrect params keys'
    assert not any([np.isnan(e) for e in params.values()]), 'params cannot have na data'

    assert params['reseed_harv_delay'] >= 1, 'harvest delay must be >=1'
    assert params['reseed_harv_delay'] % 1 < 1e5, 'harvest delay must effectively be an integer'

    # check matrix weather
    assert isinstance(matrix_weather, pd.DataFrame)
    assert set(matrix_weather.keys()) == set(_matrix_weather_keys), 'incorrect keys for matrix_weather'
    assert pd.api.types.is_integer_dtype(matrix_weather.doy), 'doy must be an integer datatype in matrix_weather'
    assert pd.api.types.is_integer_dtype(matrix_weather.year), 'year must be an integer datatype in matrix_weather'
    assert len(matrix_weather) <= _max_weather_size, 'maximum run size is {} days'.format(_max_weather_size)
    assert not matrix_weather.isna().any().any(), 'matrix_weather cannot have na values'

    # check to make sure there are no missing days in matrix_weather
    start_year = matrix_weather['year'].min()
    start_day = matrix_weather.loc[matrix_weather.year == start_year, 'doy'].min()

    stop_year = matrix_weather['year'].max()
    stop_day = matrix_weather.loc[matrix_weather.year == stop_year, 'doy'].max()

    if run_365_calendar:
        assert matrix_weather.doy.max() <= 365, 'expected to have leap days removed, and all doy between 1-365'
        doy_day_mapper = get_month_day_to_nonleap_doy()
        inv_doy_mapper = get_month_day_to_nonleap_doy(key_doy=True)
        start_mon, start_dom = inv_doy_mapper[start_day]
        stop_mon, stop_dom = inv_doy_mapper[stop_day]
        expected_datetimes = pd.date_range(start=f'{start_year}-{start_mon:02d}-{start_dom:02d}',
                                           end=f'{stop_year}-{stop_mon:02d}-{stop_dom:02d}')
        expected_datetimes = expected_datetimes[~((expected_datetimes.month == 2) & (expected_datetimes.day == 29))]
        expected_years = expected_datetimes.year.values
        expected_days = np.array(
            [doy_day_mapper[(m, d)] for m, d in zip(expected_datetimes.month, expected_datetimes.day)])
        addmess = ' note that leap days are expected to have been removed from matrix weather'
    else:
        expected_datetimes = pd.date_range(start=pd.to_datetime('{}-{}'.format(start_year, start_day), format='%Y-%j'),
                                           end=pd.to_datetime('{}-{}'.format(stop_year, stop_day), format='%Y-%j'))
        expected_years = expected_datetimes.year.values
        expected_days = expected_datetimes.dayofyear.values
        addmess = ''

    check = ((matrix_weather['year'].values == expected_years).all() and
             (matrix_weather['doy'].values == expected_days).all())
    assert check, 'the date range of matrix_weather contains missing or duplicate days' + addmess

    # check harvest data
    assert isinstance(days_harvest, pd.DataFrame)
    assert set(days_harvest.keys()) == set(days_harvest_keys), 'incorrect keys for days_harvest'
    assert pd.api.types.is_integer_dtype(days_harvest.doy), 'doy must be an integer datatype in days_harvest'
    assert pd.api.types.is_integer_dtype(days_harvest.year), 'year must be an integer datatype in days_harvest'
    assert not days_harvest.isna().any().any(), 'days_harvest cannot have na data'
    assert (days_harvest['frac_harv'] <= 1).all(), 'frac_harv cannot be greater than 1'
    if run_365_calendar:
        assert days_harvest.doy.max() <= 365
    if params['fixed_removal'] > 0.9:
        assert (days_harvest['harv_trig'] >=
                days_harvest['harv_targ']).all(), 'when using fixed harvest mode the harv_trig>=harv_targ'

    if auto_harvest:
        assert len(matrix_weather) == len(
            days_harvest), 'days_harvest and matrix_weather must be the same length(ndays)'

        check = (days_harvest['year'].values == matrix_weather.year.values).all() and (
                days_harvest['doy'].values == matrix_weather.doy.values).all()
        assert check, 'the date range of days_harvest does not match matrix_weather' + addmess
    else:
        if run_365_calendar:
            mapper = get_month_day_to_nonleap_doy(key_doy=True)
            strs = [f'{y}-{mapper[doy][0]:02d}-{mapper[doy][1]:02d}' for y, doy in zip(days_harvest.year.values,
                                                                                       days_harvest.doy.values)]
            harvest_dt = pd.to_datetime(strs)

        else:
            strs = ['{}-{:03d}'.format(int(e), int(f)) for e, f in
                    days_harvest[['year', 'doy']].itertuples(False, None)]
            harvest_dt = pd.to_datetime(strs, format='%Y-%j')
        assert harvest_dt.min() >= expected_datetimes.min(), 'days_harvest must start at or after first day of simulation'
        assert harvest_dt.max() <= expected_datetimes.max(), 'days_harvest must stop at or before last day of simulation'

    # doy_irr tests
    assert isinstance(doy_irr, np.ndarray), 'doy_irr must be convertable to a numpy array'
    assert doy_irr.ndim == 1, 'doy_irr must be 1d'
    assert pd.api.types.is_integer_dtype(doy_irr), 'doy_irr must be integers'
    assert doy_irr.max() <= 366, 'entries doy_irr must not be greater than 366'
    assert doy_irr.min() >= 0, 'entries doy_irr must not be less than 0'

    # pass a warning if max_irr is greater than abs_max_irr
    if matrix_weather.loc[:, 'max_irr'].max() > params['abs_max_irr']:
        warn(f'maximum weather_matrix max_irr ({matrix_weather.loc[:, "max_irr"].max()}) > absolute maximum '
             f'irrigation {params["abs_max_irr"]}.  The extra irrigation can never be applied but may be available for '
             f'storage.')


def get_month_day_to_nonleap_doy(key_doy=False):
    """

    :param key_doy: bool, if true the keys are doy, else keys are (month, dayofmonth)
    :return: dictionary if not inverse: {(m,d}:doy} if inverse: {doy: (m,d)}
    """
    temp = pd.date_range('2025-01-01', '2025-12-31')  # a random non leap year
    day = temp.day
    month = temp.month
    doy = temp.dayofyear
    if key_doy:
        out = {dd: (m, d) for m, d, dd in zip(month, day, doy)}
    else:
        out = {(m, d): dd for m, d, dd in zip(month, day, doy)}

    return out


if __name__ == '__main__':
    pass
