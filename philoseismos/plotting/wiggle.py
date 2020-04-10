""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np


def wiggle_dm_into(data_matrix, ax, norm=True):
    """ Display the Data Matrix in form of the seismic wiggle trace image.

    Args:
        data_matrix: A SegYs DataMatrix object.
        ax: matplotlib Axes object to draw on.
        norm (bool): Enable or disable normalization of the traces (individual).

    """

    for i, trace in enumerate(data_matrix._m):
        j = i + 1

        if norm and not np.all(trace == 0):
            trace /= np.abs(trace).max() * 0.5

        ax.plot(trace + j, data_matrix.t, color='k')
        ax.fill_betweenx(data_matrix.t, trace + j, j,
                         where=((trace + j) >= j),
                         color='k')

    ax.invert_yaxis()
