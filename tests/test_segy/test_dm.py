""" philoseismos: engineering seismologist's toolbox.

This file contains tests for DataMatrix object.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest
import numpy as np

from philoseismos.segy.dm import DataMatrix
from philoseismos.segy.segy import SegY
from philoseismos.segy.g import Geometry


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that DataMatrix object loads from file correctly. """

    dm = DataMatrix.load(manually_crafted_segy_file)

    # check the matrix itself, in the _m property of the DM
    assert dm._m.shape == (24, 512)
    assert dm._m.dtype == np.int16
    assert np.alltrue(dm._m == np.repeat(np.arange(1, 25)[:, np.newaxis], 512, axis=1))

    # check that time axis is constructed correctly
    assert dm.dt == 500
    assert np.alltrue(dm.t == np.arange(0, 256, 0.5))


def test_resample(manually_crafted_segy_file):
    """ Test the resample method of the DataMatrix. """

    segy = SegY.load(manually_crafted_segy_file)
    dm = segy.dm

    assert repr(dm) == 'DataMatrix: 24 traces, 512 samples, dt=500'
    assert dm._m.shape == (24, 512)
    assert np.alltrue(dm.t == np.arange(0, 256, 0.5))

    new = dm.resample(1000)
    assert repr(new) == 'DataMatrix: 24 traces, 256 samples, dt=1000'
    assert new._m.shape == (24, 256)
    assert np.alltrue(new.t == np.arange(0, 256, 1))

    new = dm.resample(2000)
    assert repr(new) == 'DataMatrix: 24 traces, 128 samples, dt=2000'
    assert new._m.shape == (24, 128)
    assert np.alltrue(new.t == np.arange(0, 256, 2))

    with pytest.raises(ValueError):
        new = dm.resample(256)


def test_filter(manually_crafted_segy_file):
    """ Test the filter method of the DataMatrix. """

    segy = SegY.load(manually_crafted_segy_file)
    dm = segy.dm

    assert isinstance(dm._headers, Geometry)
    assert dm._m.shape == (24, 512)
    assert np.alltrue(dm._headers.loc[:, 'REC_X'] == np.arange(0, 48, 2))

    new = dm.filter('REC_X', 10, 40, 2)
    assert isinstance(new._headers, Geometry)
    assert new._m.shape == (16, 512)
    assert np.alltrue(new._headers.loc[:, 'REC_X'] == np.arange(10, 42, 2))

    new = dm.filter('REC_X', 0, 24, 4)
    assert isinstance(new._headers, Geometry)
    # assert new._m.shape == (7, 512)
    assert np.alltrue(new._headers.loc[:, 'REC_X'] == np.arange(0, 28, 4))


def test_crop(manually_crafted_segy_file):
    """ Test the crop method of the DataMatrix. """

    segy = SegY.load(manually_crafted_segy_file)
    dm = segy.dm

    assert np.alltrue(dm.t == np.arange(0, 256, 0.5))
    assert dm._m.shape == (24, 512)

    new = dm.crop(128)
    assert np.alltrue(new.t == np.arange(0, 128.5, 0.5))
    assert new._m.shape == (24, 257)

    new = dm.crop(100)
    assert np.alltrue(new.t == np.arange(0, 100.5, 0.5))
    assert new._m.shape == (24, 201)

    dm.crop(128, inplace=True)
    assert np.alltrue(dm.t == np.arange(0, 128.5, 0.5))
    assert dm._m.shape == (24, 257)
