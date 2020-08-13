"""
 Author: Matt Hanson
 Created: 13/08/2020 12:08 PM
 """

import ctypes as ct


#compiled with gfortran 64, https://sourceforge.net/projects/mingwbuilds/files/host-windows/releases/4.8.1/64-bit/threads-posix/seh/x64-4.8.1-release-posix-seh-rev5.7z/download
# copiliation code: gfortran -shared -o test.dll test.f90
# this works!


test = ct.CDLL(r'C:\Users\Matt Hanson\python_projects\SLMACC_2020\test_fortran_dll\test.dll')
val = 2
print(val)
val = ct.pointer(ct.c_int(val))
val = test.sqr2(val)
print(val[0])
pass