"""
 Author: Matt Hanson
 Created: 1/09/2020 9:22 AM
 """
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import get_cmap
from matplotlib.patches import Patch
import pandas as pd
import os
from komanawa.basgra_nz_py.supporting_functions.output_metadata import get_output_metadata

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
                          rolling=None, main_kwargs={}, rolling_kwargs={}, label_rolling=False, label_main=True,
                          show=True):
    """
    plot multiple basgra results against each other

    :param data: dictionary of key: outputs of run_basgra()
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:

         ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD', 'BASAL', 'ROOTD', 'WAFC')

    :param title_str: a string to append to the front of the title
    :param rolling: None or int,  generate a rolling mean of rolling days
    :param main_kwargs: other kwargs passed directly to the plot function for the main plot
    :param rolling_kwargs: other kwargs passed directly to the plot function for the rolling average
    :param label_rolling: bool if True labels are created for the rolling plot if either is true then  creates a legend
    :param label_main: bool if True labels are created for the main plot if either is true then  creates a legend
    :param show: bool if true call plt.show before function return
    :return: axs: dict(data.keys():plt.ax)
    """
    metadata = get_output_metadata()
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
        ax.set_title(title_str + ' ' + v)
        axs[v] = ax
        ax.set_xlabel('date')
        if v in metadata.keys():
            ax.set_ylabel(metadata[v]['unit'])

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


def plot_multiple_monthly_violin_box(data, outdir=None, out_vars=_outvars, fig_size=(10, 8), title_str='',
                                     main_kwargs={}, label_main=True, show=True, violin_plot=False):
    """
    plot multiple basgra results as a violin plot each other shifts january to be in the middle.

    :param data: dictionary of key: outputs of run_basgra() grouped by the month, index=range(1,13)
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:

         ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD', 'BASAL', 'ROOTD', 'WAFC')

    :param title_str: a string to append to the front of the title
    :param main_kwargs: other kwargs passed directly to the plot function for the main plot
    :param label_main: bool if True labels are created for the main plot if either is true then  creates a legend
    :param show: bool if true call plt.show before function return
    :param violin_plot: bool if True plot violin plots if False plot boxplots
    :return: axs: dict(data.keys():plt.ax)
    """
    metadata = get_output_metadata()
    assert isinstance(data, dict)
    plot_months = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
    for k, v in data.items():
        assert isinstance(v, pd.DataFrame), 'data items must be dataframes, instead was {}'.format(type(v))
        v.loc[:, 'month'] = v.index.month

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
        ax.set_title(title_str + ' ' + v)
        axs[v] = ax
        ax.set_xlabel('month')
        if v in metadata.keys():
            ax.set_ylabel(metadata[v]['unit'])

    handles = {e: [] for e in out_vars}
    labels = {e: [] for e in out_vars}
    initialpositions = np.arange(0, 12 * n_scens, n_scens)
    for i, (k, out) in enumerate(data.items()):
        use_positions = initialpositions + i + 0.5
        for v in out_vars:
            c = colors[i]
            ax = axs[v]
            plot_data = []
            for m in plot_months:
                plot_data.append(out.loc[out.month == m, v].values)

            if violin_plot:
                parts = ax.violinplot(plot_data, positions=use_positions,
                                      showmeans=False, showmedians=True, quantiles=[[0.25, 0.75] for e in plot_data],
                                      **main_kwargs)
                for pc in parts['bodies']:
                    pc.set_facecolor(c)
                parts['cmedians'].set_color(c)
                parts['cquantiles'].set_color(c)
                parts['cmins'].set_color(c)
                parts['cmaxes'].set_color(c)
                parts['cbars'].set_color(c)
            else:
                bp = ax.boxplot(plot_data, positions=use_positions, patch_artist=True,
                                **main_kwargs)
                for element in ['boxes', 'whiskers', 'means', 'medians', 'caps']:
                    plt.setp(bp[element], color='k')
                plt.setp(bp['fliers'], markeredgecolor=c)
                for patch in bp['boxes']:
                    patch.set(facecolor=c)

            if label_main:
                labels[v].append(k)
                handles[v].append(Patch(facecolor=c))
                ax.legend(handles=handles[v], labels=labels[v])

    for k, ax in axs.items():
        ax.set_xticks(initialpositions + n_scens // 2)
        ax.set_xticklabels(['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
        # set verticle lines
        for i in np.concatenate((initialpositions, initialpositions + n_scens)):
            ax.axvline(x=i,
                       ymin=0,
                       ymax=1,
                       linestyle=':',
                       color='k',
                       alpha=0.5
                       )
        fig = ax.figure
        if outdir is not None:
            fig.savefig(os.path.join(outdir, '{}.png'.format(ax.title.get_text())))

    if show:
        plt.show()
    return axs


def plot_multiple_monthly_results(data, outdir=None, out_vars=_outvars, fig_size=(10, 8), title_str='',
                                  main_kwargs={}, label_main=True, show=True):
    """
    plot multiple basgra results against each other shifts january to be in the middle.

    :param data: dictionary of key: outputs of run_basgra() grouped by the month, index=range(1,13)
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:

         ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD','BASAL', 'ROOTD', 'WAFC')

    :param title_str: a string to append to the front of the title
    :param main_kwargs: other kwargs passed directly to the plot function for the main plot
    :param label_main: bool if True labels are created for the main plot if either is true then  creates a legend
    :param show: bool if true call plt.show before function return
    :return: axs: dict(data.keys():plt.ax)
    """

    metadata = get_output_metadata()
    assert isinstance(data, dict)
    for k, v in data.items():
        assert isinstance(v, pd.DataFrame), 'data items must be dataframes, instead was {}'.format(type(v))
        assert list(v.index) == list(range(1, 13)), 'data index must be range(1,13), instead was {}'.format(v.index)
        v.index = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        v.sort_index(inplace=True)

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
        ax.set_title(title_str + ' ' + v)
        axs[v] = ax
        ax.set_xlabel('month')
        if v in metadata.keys():
            ax.set_ylabel(metadata[v]['unit'])

    for i, (k, out) in enumerate(data.items()):
        for v in out_vars:
            ax = axs[v]
            if label_main:
                ax.plot(out.index, out[v], c=colors[i], label=k, **main_kwargs)
            else:
                ax.plot(out.index, out[v], c=colors[i], **main_kwargs)

    for ax in axs.values():
        ax.set_xticks(range(1, 13))
        ax.set_xticklabels(['Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
        if label_main:
            ax.legend()
        fig = ax.figure
        if outdir is not None:
            fig.savefig(os.path.join(outdir, '{}.png'.format(ax.title.get_text())))

    if show:
        plt.show()
    return axs


def plot_multiple_date_range(data, start_date, end_date, outdir=None, out_vars=_outvars, fig_size=(10, 8), title_str='',
                             rolling=None, main_kwargs={}, rolling_kwargs={}, label_rolling=False, label_main=True,
                             show=True):
    """
    as per plot multiple results but for a specific date range.

    :param data: dictionary of key: outputs of run_basgra()
    :param start_date: the start date for the range to be plotted
    :param end_date: the end date for the rnage to be plotted
    :param outdir: none or directory, if not None then makes outdir and saves plots
    :param out_vars: variables to make figures for, default is:

         ('WAL', 'WCLM', 'WCL', 'RAIN', 'IRRIG', 'DRAIN', 'RUNOFF', 'EVAP', 'TRAN', 'DM', 'YIELD', 'BASAL', 'ROOTD', 'WAFC')

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
    use_data = {}
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    for k, v in data.items():
        use_data[k] = v.loc[(v.index >= start_date) & (v.index <= end_date)]

    use_title = f'{start_date.date().isoformat()}_{end_date.date().isoformat()} {title_str}'
    axs = plot_multiple_results(data=use_data,
                                outdir=outdir,
                                out_vars=out_vars,
                                fig_size=fig_size,
                                title_str=use_title,
                                rolling=rolling,
                                main_kwargs=main_kwargs,
                                rolling_kwargs=rolling_kwargs,
                                label_rolling=label_rolling,
                                label_main=label_main,
                                show=show,
                                )
    return axs
