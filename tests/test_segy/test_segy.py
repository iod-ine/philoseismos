""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

from philoseismos.segy.segy import SegY


def test_loading_from_file(manually_crafted_segy_file):
    """ Test the method for loading SEG-Y files. """

    segy = SegY.load(manually_crafted_segy_file)

    # repeat tests for TFH
    assert repr(segy.tfh)[0:800] == ' ' * 800
    assert repr(segy.tfh)[800:880] == 'Alle warten auf das Licht'.ljust(80)
    assert repr(segy.tfh)[880:960] == 'fürchtet euch fürchtet euch nicht'.ljust(80)
    assert repr(segy.tfh)[960:1040] == 'die Sonne scheint mir aus den Augen'.ljust(80)
    assert repr(segy.tfh)[1040:1120] == 'sie wird heut Nacht nicht untergehen'.ljust(80)
    assert repr(segy.tfh)[1120:1200] == 'und die Welt zählt laut bis zehn'.ljust(80)
    assert repr(segy.tfh)[1200:1280] == 'Eins'.ljust(80)
    assert repr(segy.tfh)[1280:1360] == 'Hier kommt die Sonne'.ljust(80)
    assert repr(segy.tfh)[1360:] == ' ' * 1840

    # repeat tests for BFH
    assert segy.bfh['job_id'] == 666
    assert segy.bfh['sample_interval'] == 500
    assert segy.bfh['samples_per_trace'] == 512
    assert segy.bfh['sample_format'] == 3

    # repeat tests for Geometry
    assert np.alltrue(segy.g.loc[:, 'TRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'fTRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'FFID'] == 375)
    assert np.alltrue(segy.g.loc[:, 'ELEVSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'COORDSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'NUMSMP'] == 512)
    assert np.alltrue(segy.g.loc[:, 'DT'] == 500)
    assert np.alltrue(segy.g.loc[:, 'YEAR'] == 1984)
    assert np.alltrue(segy.g.loc[:, 'HOUR'] == 10)
    assert np.alltrue(segy.g.loc[:, 'MINUTE'] == 51)
    assert np.alltrue(segy.g.loc[:, 'SOU_X'] == 50)
    assert np.alltrue(segy.g.loc[:, 'SOU_Y'] == 75)
    assert np.alltrue(segy.g.loc[:, 'REC_X'] == np.arange(0, 48, 2))
    assert np.alltrue(segy.g.loc[:, 'REC_Y'] == -1)
    assert np.alltrue(segy.g.loc[:, 'CDP_X'] == np.arange(25, 49, 1))
    assert np.alltrue(segy.g.loc[:, 'CDP_Y'] == 37)
    assert np.all(segy.g._df.notna())

    # repeat tests for DataMatrix
    # check the matrix itself, in the _m property of the DM
    assert segy.dm._m.shape == (24, 512)
    assert segy.dm._m.dtype == np.int16
    assert np.alltrue(segy.dm._m == np.repeat(np.arange(1, 25)[:, np.newaxis], 512, axis=1))
    assert segy.dm.dt == 500
    assert np.alltrue(segy.dm.t == np.arange(0, 256, 0.5))

    # keep the name of the file
    assert segy.file == manually_crafted_segy_file.split('/')[-1]


def test_loading_from_little_endian_file(manually_crafted_little_endian_segy_file):
    """ Test the method for loading SEG-Y files with little-endian byte-order. """

    segy = SegY.load(manually_crafted_little_endian_segy_file)

    assert segy.bfh['job_id'] == 666
    assert segy.bfh['sample_interval'] == 500
    assert segy.bfh['samples_per_trace'] == 512
    assert segy.bfh['sample_format'] == 3
    assert np.alltrue(segy.g.loc[:, 'TRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'fTRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'FFID'] == 375)
    assert np.alltrue(segy.g.loc[:, 'ELEVSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'COORDSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'NUMSMP'] == 512)
    assert np.alltrue(segy.g.loc[:, 'DT'] == 500)
    assert np.alltrue(segy.g.loc[:, 'YEAR'] == 1984)
    assert np.alltrue(segy.g.loc[:, 'HOUR'] == 10)
    assert np.alltrue(segy.g.loc[:, 'MINUTE'] == 51)
    assert np.alltrue(segy.g.loc[:, 'SOU_X'] == 50)
    assert np.alltrue(segy.g.loc[:, 'SOU_Y'] == 75)
    assert np.alltrue(segy.g.loc[:, 'REC_X'] == np.arange(0, 48, 2))
    assert np.alltrue(segy.g.loc[:, 'REC_Y'] == -1)
    assert np.alltrue(segy.g.loc[:, 'CDP_X'] == np.arange(25, 49, 1))
    assert np.alltrue(segy.g.loc[:, 'CDP_Y'] == 37)
    assert np.all(segy.g._df.notna())

    # repeat tests for DataMatrix
    # check the matrix itself, in the _m property of the DM
    assert segy.dm._m.shape == (24, 512)
    assert segy.dm._m.dtype == np.int16
    assert np.alltrue(segy.dm._m == np.repeat(np.arange(1, 48, 2)[:, np.newaxis], 512, axis=1))
    assert segy.dm.dt == 500
    assert np.alltrue(segy.dm.t == np.arange(0, 256, 0.5))

    # keep the name of the file
    assert segy.file == manually_crafted_little_endian_segy_file.split('/')[-1]


def test_creating_from_matrix():
    """ Test the method for creating SegY objects from matrices. """

    one = np.ones(shape=(24, 100), dtype=np.float32)
    segy = SegY.from_matrix(one, sample_interval=1000)

    # relevant BFH values are filled
    assert segy.bfh['sample_format'] == 5
    assert segy.bfh['sample_interval'] == 1000
    assert segy.bfh['samples_per_trace'] == 100
    assert segy.bfh['measurement_system'] == 1
    assert segy.bfh['byte_offset_of_data'] == 3600
    assert segy.bfh['no_traces'] == 24

    # relevant trace headers are filled
    assert np.alltrue(segy.g.loc[:, 'TRACENO'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'FFID'] == 1)
    assert np.alltrue(segy.g.loc[:, 'CHAN'] == np.arange(1, 25, 1))
    assert np.alltrue(segy.g.loc[:, 'ELEVSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'COORDSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'NUMSMP'] == 100)
    assert np.alltrue(segy.g.loc[:, 'DT'] == 1000)

    # the traces are from the matrix
    assert np.alltrue(segy.dm._m == np.ones(shape=(24, 100)))
    assert segy.dm.dt == 1000
    assert np.alltrue(segy.dm.t == np.arange(0, 100, 1))

    # for a different matrix
    two = np.ones(shape=(48, 10), dtype=np.int16) * 2
    segy = SegY.from_matrix(two, sample_interval=500)
    assert segy.bfh['sample_format'] == 3
    assert segy.bfh['sample_interval'] == 500
    assert segy.bfh['samples_per_trace'] == 10
    assert segy.bfh['measurement_system'] == 1
    assert segy.bfh['byte_offset_of_data'] == 3600
    assert segy.bfh['no_traces'] == 48
    assert np.alltrue(segy.g.loc[:, 'TRACENO'] == np.arange(1, 49, 1))
    assert np.alltrue(segy.g.loc[:, 'FFID'] == 1)
    assert np.alltrue(segy.g.loc[:, 'CHAN'] == np.arange(1, 49, 1))
    assert np.alltrue(segy.g.loc[:, 'ELEVSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'COORDSC'] == -100)
    assert np.alltrue(segy.g.loc[:, 'NUMSMP'] == 10)
    assert np.alltrue(segy.g.loc[:, 'DT'] == 500)
    assert np.alltrue(segy.dm._m == np.ones(shape=(48, 10)) * 2)
    assert segy.dm.dt == 500
    assert np.alltrue(segy.dm.t == np.arange(0, 5, 0.5))
