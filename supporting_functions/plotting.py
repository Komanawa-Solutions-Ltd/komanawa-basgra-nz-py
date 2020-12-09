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
    'IRR_TARG',
    'IRR_TRIG',
    'IRRIG_DEM',
    'RYE_YIELD',
    'WEED_YIELD',
    'DM_RYE_RM',
    'DM_WEED_RM',
)


def plot_multiple_results(data, outdir=None, out_vars=_outvars, fig_size=(10, 8), title_str='',
                          rolling=None, main_kwargs={}, rolling_kwargs={}, label_rolling=False, label_main=True, show=True):
    """
    plot multiple basgra results against eachother
    :param data: dictionary of key: outputs of run_basgra()
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:
                     ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD',
                      'BASAL', 'ROOTD', 'WAFC')
    :param title_str: a string to append to the front of the title
    :param rolling: None or int,  generate a rolling mean of rolling days
    :param main_kwargs: other kwargs passed directly to the plot function for the main plot
    :param rolling_kwargs: other kwargs passed directly to the plot function for the rolling average
    :param label_rolling: bool if True labels are created for the rolling plot if either is true then  creates a legend
    :param label_main: bool if True labels are created for the main plot if either is true then  creates a legend
    :param show: bool if true call plt.show before function return
    :return: axs: dict(data.keys():plt.ax)
    """

    assert isinstance(data, dict)
    if outdir is not None:
        if not os.path.exists(outdir):
            os.makedirs(outdir)

    cmap = get_cmap('tab20')
    n_scens = len(data.keys())
    colors = [cmap(e / n_scens) for e in range(n_scens)]  # pick from color map

    axs = {}

    for v in out_vars:
        fig, ax = plt.subplots(figsize=fig_size)
        fig.autofmt_xdate()
        ax.set_title(title_str + v)
        axs[v] = ax

    for i, (k, out) in enumerate(data.items()):
        for v in out_vars:
            ax = axs[v]
            if label_main:
                ax.plot(out.index, out[v], c=colors[i], label=k, **main_kwargs)
            else:
                ax.plot(out.index, out[v], c=colors[i], **main_kwargs)
            if rolling is not None:
                assert isinstance(rolling, int), 'rolling must be None or int'
                temp = out[v].rolling(rolling).mean()
                if label_rolling:
                    ax.plot(out.index, temp, c=colors[i], label=k, **rolling_kwargs)
                else:
                    ax.plot(out.index, temp, c=colors[i], **rolling_kwargs)


    for ax in axs.values():
        if label_main or label_rolling:
            ax.legend()
        fig = ax.figure
        if outdir is not None:
            fig.savefig(os.path.join(outdir, '{}.png'.format(ax.title.get_text())))

    if show:
        plt.show()
    return axs
