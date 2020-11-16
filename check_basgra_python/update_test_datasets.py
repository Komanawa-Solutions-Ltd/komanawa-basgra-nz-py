"""
 Author: Matt Hanson
 Created: 17/11/2020 11:35 AM
 """
from check_basgra_python.test_basgra_python import *

if __name__ == '__main__':
    t = input('are you really sure you want to update all of the test data? y/n').lower()

    if t == 'y':
        functions = [
            test_org_basgra_nz,
            test_irrigation_trigger,
            test_irrigation_fraction,
            test_water_short,
            test_short_season,
            test_variable_irr_trig_targ,
            test_pet_calculation,
        ]
        for f in functions:
            f(update_data=True)
    else:
        raise ValueError('aborted')
