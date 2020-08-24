"""
 Author: Matt Hanson
 Created: 24/08/2020 10:50 AM
 """
from basgra_python import run_basgra_nz
from test_basgra_python import establish_input
from irrigation_test.get_weather_data import get_lincoln_broadfield, get_woodward_weather
from input_output_keys import _matrix_weather_keys
import matplotlib.pyplot as plt
import pandas as pd
import os

out_vars = [
    'WAL',
    'WCLM',
    'WCL',
    'RAIN',
    'IRRIG',
    'DRAIN',
    'RUNOFF',
    'EVAP',
    'TRAN',
    'DM',
    'YIELD',
    'BASAL',
    'ROOTD',
]


def run_old_basgra():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_woodward_weather()
    matrix_weather.loc[:, 'max_irr'] = 10

    params['IRRIGF'] = 0  # no irrigation
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


def run_nonirr_lincoln():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys]

    params['IRRIGF'] = 0  # no irrigation
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


def run_irr_lincoln():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys]

    params['IRRIGF'] = 1  # irrigation to 100% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


def run_irr60_lincoln():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys]

    params['IRRIGF'] = .60  # irrigation to 90% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


def run_irr_lincoln_water_short():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 5  # todo is this a good amount?
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 90  # finish at end of march

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


def run_irr_lincoln_day_short():
    params, matrix_weather, days_harvest = establish_input('lincoln')

    matrix_weather = get_lincoln_broadfield()
    matrix_weather.loc[:, 'max_irr'] = 10
    matrix_weather = matrix_weather.loc[:, _matrix_weather_keys]

    params['IRRIGF'] = .90  # irrigation to 90% of field capacity
    params['doy_irr_start'] = 305  # start irrigating in Nov
    params['doy_irr_end'] = 60  # finish at end of feb

    out = run_basgra_nz(params, matrix_weather, days_harvest, verbose=True)
    return out


scens = {
    'woodward': run_old_basgra,
    'no_irr': run_nonirr_lincoln,
    'irr': run_irr_lincoln,
    'water_short': run_irr_lincoln_water_short,
    'day_short': run_irr_lincoln_day_short,
    '60% fill': run_irr60_lincoln
}


def plot_results():
    colors = ['k', 'y', 'g', 'b', 'r', 'purple']

    figs = {}

    for v in out_vars:
        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        ax.set_title(v)
        figs[v] = ax

    for i, (k, fun) in enumerate(scens.items()):
        out = fun()
        for v in out_vars:
            ax = figs[v]
            ax.plot(out.index, out[v], c=colors[i], label=k)

    for ax in figs.values():
        ax.legend()
    plt.show()


def save_data(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for k, fun in scens.items():
        out = fun()
        strs = ['{}-{:03d}'.format(int(e), int(f)) for e, f in out[['year', 'doy']].itertuples(False, None)]
        out.loc[:, 'date'] = pd.to_datetime(strs, format='%Y-%j')
        out.set_index('date', inplace=True)
        out[out_vars].to_csv(os.path.join(outdir, '{}.csv'.format(k)))


if __name__ == '__main__':
    save_data(r"C:\matt_modelling_unbackedup\SLMACC_2020\initial_irr_tests")
    plot_results()

    # notes below
    # yeild is based on cut rates, and the harvest data is only starts in spring 2011... sum of yeidl through time
    # dry matter (DM) is lost everytime a harvest happens, which is why the lines are all janky after 2012
    # irrigation was negative to offset a big storm where it exceeded the drainage, I think I have fixed this
    # starting BASIL areas are helpful as a proxy... condsider how to use this for non-irrigated pasture
    # I don't understand what WCLM, WAL, and WCL are and why WCL, WCLM max out at < 50%
            # look up WCI, inital value of water co
            #fwcc relative saturation at field capacity
            # wcst, water contntent at saturation,
            # this is because water content at saturation is set to 55%, and field capacity is set to 70%, which leaves a full WCLM as 38.5% or so

    # todo investigate
    # what is happening in dry matter at the end of 2017, why is this shooting off, particularyly on the irrigation data???
    # for some reason runoff is always 0... I wonder if runoff is always negative?, this could be a key flaw
    # is it actually fill to n percent of field capacity, no it is N% of the amount of water required to fill to field capacity, is this a bug?, it would be more useful as a trigger value? this could be a new property...
    # look through all outputs, it would be rather instructive on how this model works, using this set of data.
    # think about making a irrigation time series from the rain data from woodward