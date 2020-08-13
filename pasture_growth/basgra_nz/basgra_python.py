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

# note python 3.8 might break this and I may want to figure that our... or I could just freeze this at 3.6.
# right now running on MRT environment, but really only numpy is needed
# compiled with gfortran 64, https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# copiliation code: compile_basgra_gfortran.bat
# loading this works!

libpath = os.path.join(os.path.dirname(__file__), 'fortran_BASGRA_NZ/BASGRA.DLL')


def run_basgra_nz(params, matrix_weather, days_harvest, ndays, nout=56):
    """
    python wrapper for the fortran BASGRA code
    changes to the fortran code may require changes to this function
    :param params: dictionary # todo, sort out
    :param matrix_weather: pandas dataframe of weather data
    :param days_harvest:
    :param ndays: number of days for the simulation, must match weather data
    :param nout: number of output variables.  output variales are defined #todo what are these and should this be internal only?
    :return:
    """

    # define keys to dfs
    param_keys = []  # todo fill
    matrix_weather_keys = []  # todo
    days_harvest_keys = []  # todo

    # thouroughly test inputs
    assert isinstance(params, dict)
    assert set(params.keys()) == set(param_keys), 'incorrect params keys'

    assert isinstance(matrix_weather, pd.DataFrame)
    assert matrix_weather.shape == (ndays, len(matrix_weather_keys))
    assert set(matrix_weather.keys()) == set(matrix_weather_keys), 'incorrect keys for matrix_weather'

    assert isinstance(days_harvest, pd.DataFrame)
    assert issubclass(days_harvest.values.dtype.type, np.integer), 'days_harvest must be integers'
    assert set(days_harvest.keys()) == days_harvest_keys, 'incorrect keys for days_harvest'

    assert isinstance(ndays, int)
    assert isinstance(nout, int)

    # define output indexs before data manipulation
    out_index = matrix_weather.index
    out_cols = [] # todo

    # copy everything
    params = deepcopy(params)
    matrix_weather = deepcopy(matrix_weather)
    days_harvest = deepcopy(days_harvest)
    ndays = deepcopy(ndays)
    nout = deepcopy(nout)

    # get variables into right python types
    params = np.array([params[e] for e in param_keys]).astype(float)
    matrix_weather = matrix_weather.values.astype(float)
    days_harvest = days_harvest.values

    y = np.zeros((ndays, nout), float)  # todo can I set these to nan's or does that break fortran


    # make pointers #todo


    # load DLL
    for_basgra = ct.CDLL(libpath)

    # run BASGRA #todo
    for_basgra.BASGRA_()

    # format results #todo
    raise NotImplementedError()

if __name__ == '__main__':
    pass
