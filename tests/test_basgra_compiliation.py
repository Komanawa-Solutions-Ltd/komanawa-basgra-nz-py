"""
created matt_dumont 
on: 7/2/24
"""
import unittest
from komanawa.basgra_nz_py.get_fortran_module import get_fortran_basgra

class TestFortranCompilation(unittest.TestCase):

        def test_fortran_compilation_supply_pet(self):
            self.assertTrue(get_fortran_basgra(True, verbose=True, recomplile=True))

        def test_fortran_compilation_supply_peyman(self):
            self.assertTrue(get_fortran_basgra(False, verbose=True, recomplile=True))