"""
This is a place to create a python wrapper for the BASGRA fortran model in fortarn_BASGRA_NZ

 Author: Matt Hanson
 Created: 12/08/2020 9:32 AM
 """
import os
import ctypes as ct
import numpy as np
import pandas as pd
from copy import deepcopy
from input_output_keys import _param_keys, _out_cols, _days_harvest_keys, _matrix_weather_keys

# compiled with gfortran 64,
# https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# compilation code: compile_basgra_gfortran.bat

# define the dll library path
_libpath = os.path.join(os.path.dirname(__file__), 'fortran_BASGRA_NZ/BASGRA_WG.DLL')
# this is the maximum number of weather days,
# it is hard coded into fortran_BASGRA_NZ/environment.f95 line 9
_max_weather_size = 36600



# define keys to dfs


def run_basgra_nz(params, matrix_weather, days_harvest, verbose=False,
                  dll_path=_libpath):
    """
    python wrapper for the fortran BASGRA code
    changes to the fortran code may require changes to this function
    runs the model for the period of the weather data
    :param params: dictionary, see input_output_keys.py for more details
    :param matrix_weather: pandas dataframe of weather data, maximum entries set in _max_weather_size in line 24
    :param days_harvest: days harvest dataframe no maximum entries
                        columns = (
                              year
                              doy
                              percent_harvest
                        )

    :param verbose: boolean, if True the fortran function prints a number of statements for debugging purposes
    :param dll_path: path to the compiled fortran DLL to use, default was made on windows 10 64 bit
    :return:
    """

    _test_basgra_inputs(params, matrix_weather, days_harvest, verbose)

    nout = len(_out_cols)
    ndays = len(matrix_weather)

    # define output indexs before data manipulation
    out_index = matrix_weather.index

    # copy everything
    params = deepcopy(params)
    matrix_weather = deepcopy(matrix_weather.loc[:, _matrix_weather_keys])
    days_harvest = deepcopy(days_harvest.loc[:, _days_harvest_keys])

    # get variables into right python types
    params = np.array([params[e] for e in _param_keys]).astype(float)
    matrix_weather = matrix_weather.values.astype(float)
    days_harvest = days_harvest.values

    # manage weather size,
    weather_size = len(matrix_weather)
    if weather_size < _max_weather_size:
        temp = np.zeros((_max_weather_size - weather_size, matrix_weather.shape[1]), float)
        matrix_weather = np.concatenate((matrix_weather, temp), 0)

    y = np.zeros((ndays, nout), float)  # cannot set these to nan's or it breaks fortran

    # make pointers
    # arrays # 99% sure this works
    params_p = np.asfortranarray(params).ctypes.data_as(ct.POINTER(ct.c_double))  # 1d array, float
    matrix_weather_p = np.asfortranarray(matrix_weather).ctypes.data_as(ct.POINTER(ct.c_double))  # 2d array, float
    days_harvest_p = np.asfortranarray(days_harvest).ctypes.data_as(ct.POINTER(ct.c_long))  # 2d array, int
    y_p = np.asfortranarray(y).ctypes.data_as(ct.POINTER(ct.c_double))  # 2d array, float

    # integers
    ndays_p = ct.pointer(ct.c_int(ndays))
    nout_p = ct.pointer(ct.c_int(nout))
    verb_p = ct.pointer(ct.c_bool(verbose))
    ndharv_p = ct.pointer(ct.c_int(len(days_harvest)))

    # load DLL
    for_basgra = ct.CDLL(_libpath)

    # run BASGRA
    for_basgra.BASGRA_(params_p, matrix_weather_p, days_harvest_p, ndays_p, nout_p, y_p, ndharv_p, verb_p)

    # format results
    y_p = np.ctypeslib.as_array(y_p, (ndays, nout))
    y_p = y_p.flatten(order='C').reshape((ndays,nout),order='F')
    y_p = pd.DataFrame(y_p, out_index, _out_cols)
    strs = ['{}-{:03d}'.format(int(e),int(f)) for e,f in y_p[['year','doy']].itertuples(False, None)]
    y_p.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    y_p.set_index('date',inplace=True)


    return y_p


def _test_basgra_inputs(params, matrix_weather, days_harvest, verbose):
    assert isinstance(verbose, bool), 'verbose must be boolean'
    assert isinstance(params, dict)
    assert set(params.keys()) == set(_param_keys), 'incorrect params keys'
    assert not any([np.isnan(e) for e in params.values()]), 'params cannot have na data'

    assert isinstance(matrix_weather, pd.DataFrame)
    assert set(matrix_weather.keys()) == set(_matrix_weather_keys), 'incorrect keys for matrix_weather'
    assert len(matrix_weather) <= _max_weather_size, 'maximum run size is {} days'.format(_max_weather_size)
    assert not matrix_weather.isna().any().any(), 'matrix_weather cannot have na values'

    assert isinstance(days_harvest, pd.DataFrame)
    assert issubclass(days_harvest.values.dtype.type, np.integer), 'days_harvest must be integers'
    assert set(days_harvest.keys()) == set(_days_harvest_keys), 'incorrect keys for days_harvest'
    assert not days_harvest.isna().any().any(), 'days_harvest cannot have na data'


if __name__ == '__main__':
    pass
