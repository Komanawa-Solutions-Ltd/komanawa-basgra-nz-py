"""
 Author: Matt Hanson
 Created: 23/10/2020 10:06 AM
 """


def convert_RH_vpa(rh, tmin, tmax):
    """
    calculate vapour pressure from rh tmin/tmax  assumes tmean is tmin+tmax/2
    :param rh: relative humidity (%, 0-100)
    :param tmin: min temperature (degrees c)
    :param tmax: max temperature (degrees c)
    :return: vapour pressure (kpa)
    """
    mean_t = (tmin + tmax) / 2
    pws = 6.11 * 10 ** (
                (7.5 * mean_t) / (237.3 + mean_t))  # in hPa https://www.weather.gov/media/epz/wxcalc/vaporPressure.pdf
    pws *= 1 / 10  # convert to kpa as needed by BASGRA
    vpa = rh / 100 * pws

    return vpa
