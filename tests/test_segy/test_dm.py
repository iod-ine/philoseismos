""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

from philoseismos.segy.dm import DataMatrix


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that DataMatrix object loads from file correctly. """

    dm = DataMatrix.load(manually_crafted_segy_file)

    # check the matrix itself, in the _m property of the DM
    assert dm._m.shape == (24, 512)
    assert dm._m.dtype == np.int16
    assert np.alltrue(dm._m == np.repeat(np.arange(1, 25)[:, np.newaxis], 512, axis=1))

    # check that time axis is constructed correctly
    assert dm.dt == 500
    assert np.allttrue(dm.t == np.arange(0, 256, 0.5))
