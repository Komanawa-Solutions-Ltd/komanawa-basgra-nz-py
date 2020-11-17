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
            test_trans_manual_harv,
            test_harv_trig_man,
            test_fixed_harvest_man,
            test_weed_fraction_auto,
            test_auto_harv_trig,
            test_weed_fixed_harv_auto,
            test_auto_harv_fixed,
            test_weed_fraction_man,

        ]
        for f in functions:
            f(update_data=True)
    else:
        raise ValueError('aborted')
