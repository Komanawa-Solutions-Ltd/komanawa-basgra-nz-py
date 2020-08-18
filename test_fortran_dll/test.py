"""
 Author: Matt Hanson
 Created: 13/08/2020 12:08 PM
 """

import ctypes as ct
import numpy as np
from copy import deepcopy

#compiled with gfortran 64, https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# copiliation code: gfortran -shared -o test.dll test.f90
# this works!



fortlib = ct.CDLL(r'C:\Users\Matt Hanson\python_projects\SLMACC_2020\test_fortran_dll\example.dll')

# setup the data
print('int')
N1 = 3
N2 = 4
nd1 = ct.pointer( ct.c_int(N1) )          # setup the pointer
nd2 = ct.pointer( ct.c_int(N2) )          # setup the pointer
pyarr = np.arange(1,N1*N2+1).reshape((N1,N2))
print(pyarr)
# call the function by passing the ctypes pointer using the numpy function:
_ = fortlib.sqr_2d_arr_int(nd1, nd2, np.ctypeslib.as_ctypes(pyarr))

print(np.ctypeslib.as_array(pyarr))

print('real')
N1 = 3
N2 = 4
nd1 = ct.pointer( ct.c_int(N1) )          # setup the pointer
nd2 = ct.pointer( ct.c_int(N2) )          # setup the pointer
pyarr2 = np.arange(1,N1*N2+1).reshape((N1,N2), order='F').astype(float)
pyarr3 = np.arange(1,N1*N2+1).reshape((N1,N2), order='C').astype(float)
print('fortran_array')
print(pyarr2)

pyarr2 = pyarr2.ctypes.data_as(ct.POINTER(ct.c_float)) #todo this works, but now I don't know how to get access to it
# call the function by passing the ctypes pointer using the numpy function:
_ = fortlib.sqr_2d_arr_real(nd1,nd2, pyarr2)

print('c array')
pyarr3 = np.asfortranarray(pyarr3)# todo this works nicely, now I just need to get access to the outdata
print(pyarr3)
pyarr3 = pyarr3.ctypes.data_as(ct.POINTER(ct.c_double)) #todo this works, but now I don't know how to get access to it
# call the function by passing the ctypes pointer using the numpy function:
_ = fortlib.sqr_2d_arr_real(nd1,nd2, pyarr3)

print(np.ctypeslib.as_array(pyarr3,(N1,N2)).flatten(order='C').reshape((N1,N2),order='F'))
pass
