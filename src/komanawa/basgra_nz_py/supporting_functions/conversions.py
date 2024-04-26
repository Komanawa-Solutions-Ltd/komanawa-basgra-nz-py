"""
 Author: Matt Hanson
 Created: 23/10/2020 10:06 AM
 """

import numpy as np


def convert_RH_vpa(rh, tmin, tmax):
    """
    calculate vapour pressure from rh tmin/tmax  assumes tmean is tmin+tmax/2 as per https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf

    :param rh: relative humidity (%, 0-100)
    :param tmin: min temperature (degrees c)
    :param tmax: max temperature (degrees c)
    :return: vapour pressure (kpa)
    """
    mean_t = (tmin + tmax) / 2
    pws = 6.11 * 10 ** (
            (7.5 * mean_t) / (237.3 + mean_t))  # in hPa
    pws *= 1 / 10  # convert to kpa as needed by BASGRA
    vpa = rh / 100 * pws

    return vpa


def convert_wind_to_2m(ws, z):
    """
    Convert wind speed measured at different heights above the soil surface to wind speed at 2 m above the surface, assuming a short grass surface. Based on FAO equation 47 in Allen et al (1998).

    :param ws: Measured wind speed [m s-1]
    :param z: Height of wind measurement above ground surface [m]
    :return: Wind speed at 2 m above the surface [m s-1]
    """

    ws = ws * (4.87 / (np.log(67.8 * z - 5.42)))
    return ws
