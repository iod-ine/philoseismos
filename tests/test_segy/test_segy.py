""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np

from philoseismos.segy.segy import SegY
from philoseismos.segy import gfunc


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


def test_loading_from_ibm_file(manually_crafted_ibm_segy_file):
    """ Test the method for loading SEG-Y files with IBM trace encoding. """

    segy = SegY.load(manually_crafted_ibm_segy_file)

    assert segy.bfh['job_id'] == 666
    assert segy.bfh['sample_interval'] == 500
    assert segy.bfh['samples_per_trace'] == 512
    assert segy.bfh['sample_format'] == 1
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
    assert segy.dm._m.dtype == np.float32
    assert np.alltrue(segy.dm._m == np.repeat(np.arange(1, 72, 3)[:, np.newaxis], 512, axis=1))
    assert segy.dm.dt == 500
    assert np.alltrue(segy.dm.t == np.arange(0, 256, 0.5))

    # keep the name of the file
    assert segy.file == manually_crafted_ibm_segy_file.split('/')[-1]


def test_saving_to_file(tmp_path):
    """ Test the method for saving SegYs to files. """

    sgy_path = tmp_path / 'saved_segy.sgy'

    s = SegY.from_matrix(np.ones(shape=(24, 512), dtype=np.int32), sample_interval=1000)

    s.bfh['job_id'] = 666
    s.g.loc[:, 'FFID'] = 981
    s.g.loc[:, 'SOU_X'] = 50
    s.g.loc[:, 'SOU_Y'] = 75
    s.g.loc[:, 'REC_X'] = (s.g.loc[:, 'CHAN'] - 1) * 2
    s.g.loc[:, 'REC_Y'] = -1
    s.g.loc[:, 'YEAR'] = 1984
    s.g.loc[:, 'HOUR'] = 10
    s.g.loc[:, 'MINUTE'] = 51
    s.g.loc[:, 'CDP_X'] = (s.g.loc[:, 'REC_X'] + s.g.loc[:, 'SOU_X']) / 2
    s.g.loc[:, 'CDP_Y'] = 37

    s.save(str(sgy_path))

    with sgy_path.open('br') as sgy:
        raw_tfh = sgy.read(3200)
        raw_bfh = sgy.read(400)
        raw_data = sgy.read()

    # TFH
    assert raw_tfh.decode('cp500') == ' ' * 3200

    # BFH
    assert struct.unpack('>i', raw_bfh[0:4])[0] == 666  # job id
    assert struct.unpack('>h', raw_bfh[16:18])[0] == 1000  # sample interval
    assert struct.unpack('>h', raw_bfh[20:22])[0] == 512  # samples per trace
    assert struct.unpack('>h', raw_bfh[24:26])[0] == 2  # sample format code

    for i in range(24):
        raw_th = raw_data[i * (240 + 512 * 4):(i + 1) * 240 + i * 512 * 4]
        raw_trace = raw_data[(i + 1) * 240 + i * 512 * 4:(i + 1) * (240 + 512 * 4)]

        # trace header
        assert struct.unpack('>i', raw_th[0:4])[0] == i + 1  # TRACENO
        assert struct.unpack('>i', raw_th[8:12])[0] == 981  # FFID - original field record number
        assert struct.unpack('>h', raw_th[68:70])[0] == -100  # ELEVSC - scalar to apply to all elevations
        assert struct.unpack('>h', raw_th[70:72])[0] == -100  # COORDSC - scalar to apply to all coordinates
        assert struct.unpack('>i', raw_th[72:76])[0] == 50 * 100  # SOU_X, with scalar applied
        assert struct.unpack('>i', raw_th[76:80])[0] == 75 * 100  # SOU_Y, with scalar applied
        assert struct.unpack('>i', raw_th[80:84])[0] == i * 2 * 100  # REC_X, with scalar applied
        assert struct.unpack('>i', raw_th[84:88])[0] == -1 * 100  # REC_Y, with scalar applied
        assert struct.unpack('>h', raw_th[114:116])[0] == 512  # NUMSMP - number of samples
        assert struct.unpack('>h', raw_th[116:118])[0] == 1000  # DT - sample interval in microseconds
        assert struct.unpack('>h', raw_th[156:158])[0] == 1984  # YEAR
        assert struct.unpack('>h', raw_th[160:162])[0] == 10  # HOUR
        assert struct.unpack('>h', raw_th[162:164])[0] == 51  # MINUTE
        assert struct.unpack('>i', raw_th[180:184])[0] == (50 + i * 2) / 2 * 100  # CDP_X, with scalar applied
        assert struct.unpack('>i', raw_th[184:188])[0] == 37 * 100  # CDP_Y, with scalar applied

        # trace
        trace = struct.unpack('>' + 512 * 'i', raw_trace)
        assert np.alltrue(np.array(trace) == 1)


def test_saving_to_ibm_file(tmp_path):
    """ Test the method for saving SegYs to files as IBM floats. """

    sgy_path = tmp_path / 'saved_ibm_segy.sgy'

    s = SegY.from_matrix(np.ones(shape=(24, 512), dtype=np.float32), sample_interval=1000)

    s.bfh['job_id'] = 666
    s.bfh['sample_format'] = 1  # this should trigger saving as IBM
    s.g.loc[:, 'FFID'] = 981
    s.g.loc[:, 'SOU_X'] = 50
    s.g.loc[:, 'SOU_Y'] = 75
    s.g.loc[:, 'REC_X'] = (s.g.loc[:, 'CHAN'] - 1) * 2
    s.g.loc[:, 'REC_Y'] = -1
    s.g.loc[:, 'YEAR'] = 1984
    s.g.loc[:, 'HOUR'] = 10
    s.g.loc[:, 'MINUTE'] = 51
    s.g.loc[:, 'CDP_X'] = (s.g.loc[:, 'REC_X'] + s.g.loc[:, 'SOU_X']) / 2
    s.g.loc[:, 'CDP_Y'] = 37

    s.save(str(sgy_path))

    with sgy_path.open('br') as sgy:
        raw_tfh = sgy.read(3200)
        raw_bfh = sgy.read(400)
        raw_data = sgy.read()

    # TFH
    assert raw_tfh.decode('cp500') == ' ' * 3200

    # BFH
    assert struct.unpack('>i', raw_bfh[0:4])[0] == 666  # job id
    assert struct.unpack('>h', raw_bfh[16:18])[0] == 1000  # sample interval
    assert struct.unpack('>h', raw_bfh[20:22])[0] == 512  # samples per trace
    assert struct.unpack('>h', raw_bfh[24:26])[0] == 1  # sample format code

    for i in range(24):
        raw_th = raw_data[i * (240 + 512 * 4):(i + 1) * 240 + i * 512 * 4]
        raw_trace = raw_data[(i + 1) * 240 + i * 512 * 4:(i + 1) * (240 + 512 * 4)]

        # trace header
        assert struct.unpack('>i', raw_th[0:4])[0] == i + 1  # TRACENO
        assert struct.unpack('>i', raw_th[8:12])[0] == 981  # FFID - original field record number
        assert struct.unpack('>h', raw_th[68:70])[0] == -100  # ELEVSC - scalar to apply to all elevations
        assert struct.unpack('>h', raw_th[70:72])[0] == -100  # COORDSC - scalar to apply to all coordinates
        assert struct.unpack('>i', raw_th[72:76])[0] == 50 * 100  # SOU_X, with scalar applied
        assert struct.unpack('>i', raw_th[76:80])[0] == 75 * 100  # SOU_Y, with scalar applied
        assert struct.unpack('>i', raw_th[80:84])[0] == i * 2 * 100  # REC_X, with scalar applied
        assert struct.unpack('>i', raw_th[84:88])[0] == -1 * 100  # REC_Y, with scalar applied
        assert struct.unpack('>h', raw_th[114:116])[0] == 512  # NUMSMP - number of samples
        assert struct.unpack('>h', raw_th[116:118])[0] == 1000  # DT - sample interval in microseconds
        assert struct.unpack('>h', raw_th[156:158])[0] == 1984  # YEAR
        assert struct.unpack('>h', raw_th[160:162])[0] == 10  # HOUR
        assert struct.unpack('>h', raw_th[162:164])[0] == 51  # MINUTE
        assert struct.unpack('>i', raw_th[180:184])[0] == (50 + i * 2) / 2 * 100  # CDP_X, with scalar applied
        assert struct.unpack('>i', raw_th[184:188])[0] == 37 * 100  # CDP_Y, with scalar applied

        # trace
        trace = gfunc.unpack_ibm32_series(raw_trace, '>')
        assert np.alltrue(np.array(trace) == 1)


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
