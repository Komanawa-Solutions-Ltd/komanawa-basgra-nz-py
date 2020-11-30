"""
 Author: Matt Hanson
 Created: 24/11/2020 9:05 AM
 """

import pandas as pd
import os
from input_output_keys import plant_param_keys, site_param_keys

def get_woodward_mean_site_param(site):
    """
    get woodward 2020 site parameters see fortran_BASGRA_NZ/docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf
    for more details
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    if site == 'scott' or site =='waikato':
        col = 1 + 8 * (1)
    elif site =='northland':
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

    params = params.loc[list(site_param_keys)]
    params = params.to_dict()

    return params

def get_woodward_mean_plant_params(site):
    """
    get woodward 2020 plant parameters see fortran_BASGRA_NZ/docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf
    for more details

    Note that the plant parameters are identical across all sites other than [LOG10CLVI, LOG10CRTI, TILTOTI, BASALI]
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    if site == 'scott' or site =='waikato':
        col = 1 + 8 * (1)
    elif site =='northland':
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

    params = params.loc[list(plant_param_keys)]
    params = params.to_dict()

    return params


def get_woodward_mean_full_params(site):
    """
    get woodward 2020 site parameters see fortran_BASGRA_NZ/docs/Woodward et al 2020 Tiller Persistence GFS Final.pdf
    for more details
    :param site: one of {'waikato': scott farm in Waikato,
                         'scott': scott farm in Waikato, used for back compatibility
                         'northland': Jordan Vally farm in northland,
                         'lincoln': Lincoln test farm in Lincoln Canterbury}

    :return:
    """
    out = {}
    out.update(get_woodward_mean_plant_params(site))
    out.update(get_woodward_mean_site_param(site))

    return out
