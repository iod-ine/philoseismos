""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np


def imshow_dm_into(data_matrix, ax, norm=True):
    """ Display the Data Matrix in form of an image.

    Args:
        data_matrix: A SegYs DataMatrix object.
        ax: matplotlib Axes object to draw on.
        norm (bool): Enable or disable normalization of the traces (individual).

    """

    if norm:
        factor = data_matrix._m.max(axis=1)
        factor[factor == 0] = 1
        normalized = data_matrix._m / factor[:, np.newaxis]
        im = ax.imshow(normalized.T, aspect='auto', cmap='binary', interpolation='gaussian')
        return im
    else:
        im = ax.imshow(data_matrix._m.T, aspect='auto', cmap='binary', interpolation='gaussian')
        return im
