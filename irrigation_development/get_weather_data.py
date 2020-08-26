"""
 Author: Matt Hanson
 Created: 21/08/2020 12:14 PM
 """

import pandas as pd
import matplotlib.pyplot as plt
from check_basgra_python.support_for_tests import get_lincoln_broadfield, get_woodward_weather


def merge_data(outpath=None):
    woodward = get_woodward_weather().reset_index()
    strs = ['{}-{:03d}'.format(e,f) for e,f in woodward[['year','doy']].itertuples(False, None)]
    woodward.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    niwa = get_lincoln_broadfield().reset_index()
    strs = ['{}-{:03d}'.format(e,f) for e,f in niwa[['year','doy']].itertuples(False, None)]
    niwa.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j') - pd.DateOffset(1) # there seems to be an off by 1 error with woodward
    joined = pd.merge(woodward,niwa,suffixes=['_wood','_niwa'],on='date')
    joined.loc[:,'rain_dif'] = joined.loc[:,'rain_wood'] - joined.loc[:,'rain_niwa']
    if outpath is not None:
        joined.to_csv(outpath)
    return joined
def plot_woodward_v_niwa():
    woodward = get_woodward_weather().reset_index()
    strs = ['{}-{:03d}'.format(e,f) for e,f in woodward[['year','doy']].itertuples(False, None)]
    woodward.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j')
    niwa = get_lincoln_broadfield().reset_index()
    strs = ['{}-{:03d}'.format(e,f) for e,f in niwa[['year','doy']].itertuples(False, None)]
    niwa.loc[:,'date'] = pd.to_datetime(strs,format='%Y-%j') - pd.DateOffset(1) # there seems to be an off by 1 error with woodward
    joined = pd.merge(woodward,niwa,suffixes=['_wood','_niwa'],on='date')

    for k in woodward.keys():
        if k in ['year','doy','date']:
            continue
        fig,(ax) = plt.subplots()
        ax.scatter(woodward.date, woodward[k],c='r',label='wood')
        ax.scatter(niwa.date, niwa[k],c='b',label='niwa')
        ax.set_title(k)
        ax.legend()

        fig,(ax) = plt.subplots()
        ax.scatter(joined['{}_niwa'.format(k)],joined['{}_wood'.format(k)])
        ax.plot(joined['{}_niwa'.format(k)],joined['{}_niwa'.format(k)])
        ax.set_xlabel('niwa')
        ax.set_ylabel('woodward')
        ax.set_title(k)

    plt.show()


if __name__ == '__main__':
    out = merge_data(r"C:\matt_modelling_unbackedup\SLMACC_2020\niwa_woodward_data.csv")
    fig, ax = plt.subplots()
    ax.scatter(out.loc[:,'date'], out.rain_dif)
    plot_woodward_v_niwa()
    plt.show()
