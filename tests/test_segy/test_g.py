""" philoseismos: engineering seismologist's toolbox.

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
    assert np.alltrue(g.loc[:, 'FFID'].values == 375)
    assert np.alltrue(g.loc[:, 'ELEVSC'].values == -100)
    assert np.alltrue(g.loc[:, 'COORDSC'].values == -100)
    assert np.alltrue(g.loc[:, 'NUMSMP'].value == 512)
    assert np.alltrue(g.loc[:, 'DT'].value == 500)
    assert np.alltrue(g.loc[:, 'YEAR'].value == 1984)
    assert np.alltrue(g.loc[:, 'HOUR'].value == 10)
    assert np.alltrue(g.loc[:, 'MINUTE'].value == 51)

    # scalars to coordinates and elevations should be applied automatically
    assert np.alltrue(g.loc[:, 'SOU_X'].values == 50)
    assert np.alltrue(g.loc[:, 'SOU_Y'].values == 75)
    assert np.alltrue(g.loc[:, 'REC_X'].values == np.arange(0, 48, 2))
    assert np.alltrue(g.loc[:, 'REC_Y'].value == -1)
    assert np.alltrue(g.loc[:, 'CDP_X'].value == np.arange(25, 49, 1))
    assert np.alltrue(g.loc[:, 'CDP_Y'].value == 37)
