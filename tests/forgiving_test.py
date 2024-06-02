"""
 Author: Matt Hanson
 Created: 14/10/2021 10:52 AM
 """

from test_basgra_python import *

all_checks = [
    'test_org_basgra_nz',
    'test_irrigation_trigger',
    'test_irrigation_fraction',
    'test_water_short',
    'test_short_season',
    'test_variable_irr_trig_targ',
    'test_pet_calculation',
    'test_trans_manual_harv',
    'test_harv_trig_man',
    'test_fixed_harvest_man',
    'test_weed_fraction_auto',
    'test_auto_harv_trig',
    'test_weed_fixed_harv_auto',
    'test_auto_harv_fixed',
    'test_weed_fraction_man',
    'test_irr_paw',
    'test_reseed',
    'test_leap',
    'test_pass_soil_mosit',
    'test_full_refill',
    'test_runoff_from_rain',
    'test_external_rainfall_runoff',
    'test_leakage_prescribed_outflow',
    'test_store_irr_org_demand',
    'test_store_irr_ind_demand',
    'test_store_irr_org_demand_paw',
    'test_store_irr_ind_demand_paw',
    'test_store_refill_from_scheme',

]


def forgiving_test():
    exceptions = []
    for t in all_checks:
        try:
            eval(t)()
        except Exception as val:
            exceptions.append(f'\n\n{t} failed: \n\n {val}')
    for v in exceptions:
        print(v)
if __name__ == '__main__':
    forgiving_test()