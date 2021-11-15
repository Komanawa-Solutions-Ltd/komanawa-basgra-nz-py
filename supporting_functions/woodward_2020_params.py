"""
 Author: Matt Hanson
 Created: 24/11/2020 9:05 AM
 """

import pandas as pd
import os
from input_output_keys import plant_param_keys, site_param_keys


def get_woodward_mean_site_param(site):
    """
    get woodward 2020 site parameters see Woodward, 2020 https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464
    for more details
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    params = pd.Series(get_woodward_mean_full_params(site))
    params = params.loc[list(site_param_keys)]
    params.to_dict()
    return params


def get_woodward_mean_plant_params(site):
    """
    get woodward 2020 plant parameters see Woodward, 2020 https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464
    for more details

    Note that the plant parameters are identical across all sites other than [LOG10CLVI, LOG10CRTI, TILTOTI, BASALI]
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    params = pd.Series(get_woodward_mean_full_params(site))
    params = params.loc[list(plant_param_keys)]
    params.to_dict()
    return params


def get_woodward_mean_full_params(site):
    """
    get woodward 2020 site parameters see Woodward, 2020 https://onlinelibrary.wiley.com/doi/abs/10.1111/gfs.12464
    for more details
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    if site == 'scott' or site == 'waikato':
        col = 1 + 8 * (1)
    elif site == 'northland':
        col = 1 + 8 * (1 - 1)
    elif site == 'lincoln':
        col = 1 + 8 * (3 - 1)
    else:
        raise ValueError('unexpected site')
    params = pd.read_csv(os.path.join(os.path.dirname(__file__), 'Woodward_2020_BASGRA_parModes.txt'),
                         delim_whitespace=True, index_col=0).iloc[:, col]
    params.loc['IRRIGF'] = 0
    params.loc['fixed_removal'] = 0
    params.loc['DRATE'] = 50  # used to be set inside fortran
    params.loc['CO2A'] = 350  # used to be set inside fortran
    params.loc['poolInfilLimit'] = 0.2  # used to be set inside fortran
    params.loc['opt_harvfrin'] = 0
    params.loc['irr_frm_paw'] = 0
    params.loc['reseed_harv_delay'] = 1
    params.loc['reseed_LAI'] = 0
    params.loc['reseed_TILG2'] = 0
    params.loc['reseed_TILG1'] = 0
    params.loc['reseed_TILV'] = 0
    params.loc['reseed_CLV'] = 0
    params.loc['reseed_CRES'] = 0
    params.loc['reseed_CST'] = 0
    params.loc['reseed_CSTUB'] = 0
    params.loc['pass_soil_moist'] = 0

    params.loc['use_storage'] = 0
    # the following storage parameters should not matter if use_storage == 0
    params.loc['runoff_from_rain'] = 1
    params.loc['calc_ind_store_demand'] = 0

    params.loc['stor_full_refil_doy'] = 240
    params.loc['abs_max_irr'] = 1000  # non-sensically high
    params.loc['irrigated_area'] = 100  # set to ensure that use_storage=0 cuts storage
    params.loc['I_h2o_store_vol'] = 0
    params.loc['h2o_store_max_vol'] = 10000
    params.loc['h2o_store_SA'] = 0
    params.loc['runoff_area'] = 0
    params.loc['runoff_frac'] = 0
    params.loc['stor_refill_min'] = 0
    params.loc['stor_refill_losses'] = 0
    params.loc['stor_leakage'] = 0
    params.loc['stor_irr_ineff'] = 0
    params.loc['stor_reserve_vol'] = 0

    params = params.to_dict()

    return params
