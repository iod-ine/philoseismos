""" philoseismos: engineering seismologist's toolbox.

This file contains tests for the Geometry object.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

from philoseismos.segy.g import Geometry


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that Geometry object loads from file correctly. """

    g = Geometry.load(manually_crafted_segy_file)

    # geometry should behave like a pd.DataFrame.
    # main way to access data is .loc property

    # check that all the headers are correctly loaded
    assert np.alltrue(g.loc[:, 'TRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(g.loc[:, 'fTRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(g.loc[:, 'FFID'] == 375)
    assert np.alltrue(g.loc[:, 'ELEVSC'] == -100)
    assert np.alltrue(g.loc[:, 'COORDSC'] == -100)
    assert np.alltrue(g.loc[:, 'NUMSMP'] == 512)
    assert np.alltrue(g.loc[:, 'DT'] == 500)
    assert np.alltrue(g.loc[:, 'YEAR'] == 1984)
    assert np.alltrue(g.loc[:, 'HOUR'] == 10)
    assert np.alltrue(g.loc[:, 'MINUTE'] == 51)

    # scalars to coordinates and elevations should be applied automatically
    assert np.alltrue(g.loc[:, 'SOU_X'] == 50)
    assert np.alltrue(g.loc[:, 'SOU_Y'] == 75)
    assert np.alltrue(g.loc[:, 'REC_X'] == np.arange(0, 48, 2))
    assert np.alltrue(g.loc[:, 'REC_Y'] == -1)
    assert np.alltrue(g.loc[:, 'CDP_X'] == np.arange(25, 49, 1))
    assert np.alltrue(g.loc[:, 'CDP_Y'] == 37)

    # there should be no NaN values in the Geometry
    assert np.all(g._df.notna())


def test_apply_coordinate_scalar_after_unpacking(geometry):
    """ Test that scalars for coordinates and elevations are applied correctly. """

    # if positive, scalar is used as a multiplier
    geometry.loc[:, 'ELEVSC'] = 10
    geometry.loc[:, 'COORDSC'] = 10
    geometry._apply_scalars_after_unpacking()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 1000)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 2000)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 3000)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 4000)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 5000)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 6000)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 7000)

    # if negative, scalar is used as divisor
    geometry.loc[:, 'ELEVSC'] = -100
    geometry.loc[:, 'COORDSC'] = -100
    geometry._apply_scalars_after_unpacking()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 10)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 20)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 30)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 40)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 50)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 60)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 70)

    # value of zero is assumed to be a scalar value of 1
    geometry.loc[:, 'ELEVSC'] = 0
    geometry.loc[:, 'COORDSC'] = 0
    geometry._apply_scalars_after_unpacking()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 10)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 20)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 30)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 40)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 50)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 60)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 70)


def test_apply_coordinate_scalar_before_packing(geometry):
    """ Test that scalars are applied correctly before packing. """

    # when unpacking: if positive, scalar is used as a multiplier
    # so we reverse it here
    geometry.loc[:, 'ELEVSC'] = 10
    geometry.loc[:, 'COORDSC'] = 10
    geometry._apply_scalars_before_packing()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 10)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 20)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 30)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 40)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 50)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 60)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 70)

    # when unpacking: if negative, scalar is used as divisor
    # again reverse that
    geometry.loc[:, 'ELEVSC'] = -100
    geometry.loc[:, 'COORDSC'] = -100
    geometry._apply_scalars_before_packing()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 1000)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 2000)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 3000)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 4000)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 5000)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 6000)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 7000)

    # value of zero is assumed to be a scalar value of 1
    geometry.loc[:, 'ELEVSC'] = 0
    geometry.loc[:, 'COORDSC'] = 0
    geometry._apply_scalars_before_packing()

    assert np.alltrue(geometry.loc[:, 'REC_ELEV'] == 1000)
    assert np.alltrue(geometry.loc[:, 'SOU_ELEV'] == 2000)
    assert np.alltrue(geometry.loc[:, 'DEPTH'] == 3000)
    assert np.alltrue(geometry.loc[:, 'REC_DATUM'] == 4000)
    assert np.alltrue(geometry.loc[:, 'SOU_DATUM'] == 5000)
    assert np.alltrue(geometry.loc[:, 'SOU_H2OD'] == 6000)
    assert np.alltrue(geometry.loc[:, 'REC_H2OD'] == 7000)
