"""
 Author: Matt Hanson
 Created: 13/08/2020 12:08 PM
 """

import ctypes as ct
import numpy as np

#compiled with gfortran 64, https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# copiliation code: gfortran -shared -o test.dll test.f90
# this works!



fortlib = ct.CDLL(r'C:\Users\Matt Hanson\python_projects\SLMACC_2020\test_fortran_dll\example.dll')

# setup the data
print('int')
N = 3
nd = ct.pointer( ct.c_int(N) )          # setup the pointer
pyarr = np.arange(1,N**2+1).reshape((N,N))
print(pyarr)
# call the function by passing the ctypes pointer using the numpy function:
_ = fortlib.sqr_2d_arr_int(nd, np.ctypeslib.as_ctypes(pyarr))

print(np.ctypeslib.as_array(pyarr))

print('real')
N = 3
nd = ct.pointer( ct.c_int(N) )          # setup the pointer
pyarr2 = np.arange(1,N**2+1).reshape((N,N)).astype(float)
print(pyarr2)
# call the function by passing the ctypes pointer using the numpy function:
_ = fortlib.sqr_2d_arr_real(nd, np.ctypeslib.as_ctypes(pyarr2))

print(np.ctypeslib.as_array(pyarr2))
pass