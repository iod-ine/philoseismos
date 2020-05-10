""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
from matplotlib import ticker


def wiggle_dm_into(data_matrix, ax, norm=True, label_header=None, label_header_step=1):
    """ Display the Data Matrix in form of the seismic wiggle trace image.

    Args:
        data_matrix: A SegY's DataMatrix object.
        ax: matplotlib Axes object to draw on.
        norm (bool): Enable or disable normalization of the traces (individual).
        label_header (str): Header name to use as label for x axis.
        label_header_step (int): Step to use when labeling traces with label_header values.

    """

    for i, trace in enumerate(data_matrix._m):

        if norm and not np.all(trace == 0):
            trace /= np.abs(trace).max() * 2

        ax.plot(trace + i, data_matrix.t, color='k', lw=1)
        ax.fill_betweenx(data_matrix.t, trace + i, i, where=((trace + i) >= i), color='k')

    ntraces = data_matrix._m.shape[0]
    ax.set_xlim(-1, ntraces)
    ax.set_ylim(0, data_matrix.t.max())

    if label_header:
        labels = data_matrix._headers.loc[::label_header_step, label_header].values
        ax.xaxis.set_major_locator(ticker.FixedLocator(range(0, ntraces, label_header_step)))
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))

    ax.invert_yaxis()
