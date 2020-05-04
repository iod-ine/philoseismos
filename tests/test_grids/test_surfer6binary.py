""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
import pytest

from philoseismos.grids import Surfer6BinaryGrid


def test_loading_surfer6binary(grd_file, bad_grd_file):
    """ Test loading process of the grid files. """

    # only proceeds to read true .grd files
    with pytest.raises(ValueError):
        grd = Surfer6BinaryGrid.load(bad_grd_file)

    grd = Surfer6BinaryGrid.load(grd_file)

    assert grd.nx == 10
    assert grd.ny == 15
    assert grd.xlo == 0
    assert grd.xhi == 9
    assert grd.ylo == 10
    assert grd.yhi == 38
    assert grd.zlo == 0
    assert grd.zhi == 150

    assert grd.dm.shape == (15, 10)
    assert np.alltrue(grd.dm == np.arange(150).reshape(15, 10))


def test_surfer6binary_properties(grd_file):
    """ Test the properties of the grid. """

    grd = Surfer6BinaryGrid.load(grd_file)

    # to help construct the plt.imshow, grid returns it's extent
    assert grd.extent == [0, 9, 38, 10]


def test_surfer6binary_invert_axis_methods(grd_file):
    """ Test the .invert_yaxis() and .invert_xaxis() method of the gird. """

    grd = Surfer6BinaryGrid.load(grd_file)

    dm = np.arange(150).reshape(15, 10)

    assert np.alltrue(grd.dm == dm)
    assert grd.ylo == 10
    assert grd.yhi == 38
    assert grd.xhi == 9
    assert grd.xlo == 0
    grd.invert_yaxis()
    assert np.alltrue(grd.dm == dm[::-1, :])
    assert grd.ylo == 38
    assert grd.yhi == 10
    grd.invert_xaxis()
    assert np.alltrue(grd.dm == dm[::-1, ::-1])
    assert grd.xlo == 9
    assert grd.xhi == 0
    grd.invert_yaxis()
    assert np.alltrue(grd.dm == dm[:, ::-1])
    grd.invert_xaxis()
    assert np.alltrue(grd.dm == dm)
    assert grd.ylo == 10
    assert grd.yhi == 38
    assert grd.xhi == 9
    assert grd.xlo == 0
