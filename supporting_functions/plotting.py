"""
 Author: Matt Hanson
 Created: 1/09/2020 9:22 AM
 """
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import os

_outvars = (
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
    'WAFC',
)


def plot_multiple_results(data, outdir=None, out_vars=_outvars):
    """
    plot multiple basgra results against eachother
    :param data: dictionary of key: outputs of run_basgra()
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:
                     ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD',
                      'BASAL', 'ROOTD', 'WAFC')
    :return:
    """

    assert isinstance(data, dict)
    if outdir is not None:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    cmap = get_cmap('tab20')
    n_scens = len(data.keys())
    colors = [cmap(e/n_scens) for e in range(n_scens)] # pick from color map

    figs = {}

    for v in out_vars:
        fig, ax = plt.subplots()
        fig.autofmt_xdate()
        ax.set_title(v)
        figs[v] = ax

    for i, (k, out) in enumerate(data.items()):
        for v in out_vars:
            ax = figs[v]
            ax.plot(out.index, out[v], c=colors[i], label=k)

    for ax in figs.values():
        ax.legend()
        fig = ax.figure
        if outdir is not None:
            fig.savefig(os.path.join(outdir, '{}.png'.format(ax.title.get_text())))

    if outdir is None:
        plt.show()