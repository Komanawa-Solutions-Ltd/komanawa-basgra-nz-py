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
from pasture_growth.basgra_nz.input_output_keys import _param_keys, _out_cols, _days_harvest_keys, _matrix_weather_keys

# note python 3.8 might break this and I may want to figure that our... or I could just freeze this at 3.6.
# right now running on MRT environment, but really only numpy is needed
# compiled with gfortran 64, https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# copiliation code: compile_basgra_gfortran.bat
# loading this works!

# define the dll library path
_libpath = os.path.join(os.path.dirname(__file__), 'fortran_BASGRA_NZ/BASGRA.DLL')


# define keys to dfs


def run_basgra_nz(params, matrix_weather, days_harvest, ndays):
    """
    python wrapper for the fortran BASGRA code
    changes to the fortran code may require changes to this function
    :param params: dictionary, see input_output_keys.py for more details
    :param matrix_weather: pandas dataframe of weather data
    :param days_harvest: days harvest dataframe columns = (
                              year
                              doy
                              percent_harvest
                        )
                        the null values and assumed size system is managed internally
    :param ndays: number of days for the simulation, must match weather data, todo can this be moved internnaly?
    :return:
    """

    # todo it may be worth passin Nmax days (e.g. for weather) and harvest dimensions to the basgra function

    # thouroughly test inputs
    assert isinstance(params, dict)
    assert set(params.keys()) == set(_param_keys), 'incorrect params keys'

    assert isinstance(matrix_weather, pd.DataFrame)
    assert matrix_weather.shape == (ndays, len(_matrix_weather_keys))
    assert set(matrix_weather.keys()) == set(_matrix_weather_keys), 'incorrect keys for matrix_weather'

    assert isinstance(days_harvest, pd.DataFrame)
    assert issubclass(days_harvest.values.dtype.type, np.integer), 'days_harvest must be integers'
    assert set(days_harvest.keys()) == _days_harvest_keys, 'incorrect keys for days_harvest'
    # todo manage days_harvest size, currently cannot be greater than 100, could this be set as an unbounded array?  I don't know, otherwise we could make it excessivly large

    assert isinstance(ndays, int)

    nout = len(_out_cols)

    # define output indexs before data manipulation
    out_index = matrix_weather.index  # todo this should maybe be defined a bit better...

    # copy everything
    params = deepcopy(params)
    matrix_weather = deepcopy(matrix_weather[_matrix_weather_keys])
    days_harvest = deepcopy(days_harvest[_days_harvest_keys])
    ndays = deepcopy(ndays)
    nout = deepcopy(nout)

    # get variables into right python types
    params = np.array([params[e] for e in _param_keys]).astype(float)
    matrix_weather = matrix_weather.values.astype(float)
    days_harvest = days_harvest.values

    y = np.zeros((ndays, nout), float)  # cannot set these to nan's or it breaks fortran

    # make pointers

    # arrays # 99% sure this works
    params_p = np.ctypeslib.as_ctypes(params)  # 1d array, float
    matrix_weather_p = np.ctypeslib.as_ctypes(matrix_weather)  # 2d array, float
    days_harvest_p = np.ctypeslib.as_ctypes(days_harvest)  # 2d array, int
    y_p = np.ctypeslib.as_ctypes(y)  # 2d array, float

    # integers
    ndays_p = ct.pointer(ct.c_int(ndays))
    nout_p = ct.pointer(ct.c_int(nout))

    # load DLL
    for_basgra = ct.CDLL(_libpath)

    # run BASGRA #todo test
    for_basgra.BASGRA_(params_p, matrix_weather_p, days_harvest_p, ndays_p, nout_p, y_p)

    # format results
    y_p = np.ctypeslib.as_array(y_p)
    y_p = pd.DataFrame(y_p, out_index,_out_cols)

    return y_p


if __name__ == '__main__':
    pass
