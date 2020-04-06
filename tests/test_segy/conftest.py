""" philoseismos: engineering seismologist's toolbox.

This file contains fixtures that are used for testing SEG-Y functionality of philoseismos.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest
import struct
import numpy as np
import pandas as pd

from philoseismos.segy.g import Geometry
from philoseismos.segy import gfunc
from philoseismos.segy import constants as const


@pytest.fixture(scope='package')
def manually_crafted_segy_file(tmp_path_factory):
    """ Return a path to a manually crafted SEG-Y (big endian) file to run tests against.

    File produced by this code was checked in SeiSee, RadExPro, and Prism 2.
    It is opened and interpreted as intended by all three of these programs.

    """

    path = str(tmp_path_factory.mktemp('manual') / 'test_segy.sgy')

    with open(path, 'bw') as sgy:
        # first 3200 bytes are for textual file header.
        # textual file header is a human-readable description of the data.
        # it contains 40 lines of 80 characters

        # create a list of empty lines
        tfh_lines = [' ' * 80 for i in range(40)]

        # set some of the lines to Rammstein's Sonne
        tfh_lines[10] = 'Alle warten auf das Licht'.ljust(80)
        tfh_lines[11] = 'fürchtet euch fürchtet euch nicht'.ljust(80)
        tfh_lines[12] = 'die Sonne scheint mir aus den Augen'.ljust(80)
        tfh_lines[13] = 'sie wird heut Nacht nicht untergehen'.ljust(80)
        tfh_lines[14] = 'und die Welt zählt laut bis zehn'.ljust(80)
        tfh_lines[15] = 'Eins'.ljust(80)
        tfh_lines[16] = 'Hier kommt die Sonne'.ljust(80)

        # standard encoding is EBCDIC, or cp500
        tfh = ''.join(tfh_lines).encode('cp500')
        sgy.write(tfh)

        # then go 400 bytes of binary file header.
        # it contains binary values relevant to the whole file
        bfh = bytearray(400)
        bfh[0:4] = struct.pack('>i', 666)  # job id
        bfh[16:18] = struct.pack('>h', 500)  # sample interval in microseconds
        bfh[20:22] = struct.pack('>h', 512)  # number of samples per trace
        bfh[24:26] = struct.pack('>h', 3)  # sample format code
        sgy.write(bfh)

        # then go the traces. each trace has a 240 byte header, and some number of samples.
        # construct a fixed part of the trace header first
        tr_hdr = bytearray(240)
        tr_hdr[8:12] = struct.pack('>i', 375)  # FFID - original field record number
        tr_hdr[68:70] = struct.pack('>h', -100)  # ELEVSC - scalar to apply to all elevations
        tr_hdr[70:72] = struct.pack('>h', -100)  # COORDSC - scalar to apply to all coordinates
        tr_hdr[72:76] = struct.pack('>i', 50 * 100)  # SOU_X, with scalar applied
        tr_hdr[76:80] = struct.pack('>i', 75 * 100)  # SOU_Y, with scalar applied
        tr_hdr[84:88] = struct.pack('>i', -1 * 100)  # REC_Y, with scalar applied
        tr_hdr[114:116] = struct.pack('>h', 512)  # NUMSMP - number of samples in a trace
        tr_hdr[116:118] = struct.pack('>h', 500)  # DT - sample interval for this trace in microseconds
        tr_hdr[156:158] = struct.pack('>h', 1984)  # YEAR
        tr_hdr[160:162] = struct.pack('>h', 10)  # HOUR
        tr_hdr[162:164] = struct.pack('>h', 51)  # MINUTE
        tr_hdr[184:188] = struct.pack('>i', 37 * 100)  # CDP_Y, with scalar applied

        for i in range(24):
            # these parts of trace header are different for all traces
            tr_hdr[0:4] = struct.pack('>i', i + 1)  # trace number within a line
            tr_hdr[4:8] = struct.pack('>i', i + 1)  # trace number within a file
            tr_hdr[80:84] = struct.pack('>i', i * 2 * 100)  # REC_X, with scalar applied
            tr_hdr[180:184] = struct.pack('>i', int((50 + i * 2) / 2 * 100))  # CDP_X, with scalar applied
            sgy.write(tr_hdr)

            tr_val = np.ones(512, dtype=np.int16) + i
            tr_bytes = struct.pack('>' + 'h' * 512, *tr_val)
            sgy.write(tr_bytes)

    return path


@pytest.fixture(scope='package')
def manually_crafted_little_endian_segy_file(tmp_path_factory):
    """ Return a path to a manually crafted SEG-Y (little endian) file to run tests against.

    File produced by this code was also checked in SeiSee, RadExPro, and Prism 2.
    It is opened and interpreted as intended by all three of these programs.

    """

    path = str(tmp_path_factory.mktemp('manual') / 'test_segy_little_endian.sgy')

    with open(path, 'bw') as sgy:
        # empty TFH
        sgy.write(bytes(3200))

        # same BFH
        bfh = bytearray(400)
        bfh[0:4] = struct.pack('<i', 666)  # job id
        bfh[16:18] = struct.pack('<h', 500)  # sample interval in microseconds
        bfh[20:22] = struct.pack('<h', 512)  # number of samples per trace
        bfh[24:26] = struct.pack('<h', 3)  # sample format code
        sgy.write(bfh)

        # same trace headers
        tr_hdr = bytearray(240)
        tr_hdr[8:12] = struct.pack('<i', 375)  # FFID
        tr_hdr[68:70] = struct.pack('<h', -100)  # ELEVSC
        tr_hdr[70:72] = struct.pack('<h', -100)  # COORDSC
        tr_hdr[72:76] = struct.pack('<i', 50 * 100)  # SOU_X, with scalar applied
        tr_hdr[76:80] = struct.pack('<i', 75 * 100)  # SOU_Y, with scalar applied
        tr_hdr[84:88] = struct.pack('<i', -1 * 100)  # REC_Y, with scalar applied
        tr_hdr[114:116] = struct.pack('<h', 512)  # NUMSMP
        tr_hdr[116:118] = struct.pack('<h', 500)  # DT
        tr_hdr[156:158] = struct.pack('<h', 1984)  # YEAR
        tr_hdr[160:162] = struct.pack('<h', 10)  # HOUR
        tr_hdr[162:164] = struct.pack('<h', 51)  # MINUTE
        tr_hdr[184:188] = struct.pack('<i', 37 * 100)  # CDP_Y, with scalar applied

        for i in range(24):
            tr_hdr[0:4] = struct.pack('<i', i + 1)  # trace number within a line
            tr_hdr[4:8] = struct.pack('<i', i + 1)  # trace number within a file
            tr_hdr[80:84] = struct.pack('<i', i * 2 * 100)  # REC_X, with scalar applied
            tr_hdr[180:184] = struct.pack('<i', int((50 + i * 2) / 2 * 100))  # CDP_X, with scalar applied
            sgy.write(tr_hdr)
            tr_val = np.ones(512, dtype=np.int16) + i * 2
            tr_bytes = struct.pack('<' + 'h' * 512, *tr_val)
            sgy.write(tr_bytes)

    return path


@pytest.fixture(scope='package')
def manually_crafted_ibm_segy_file(tmp_path_factory):
    """ Return a path to a manually crafted SEG-Y (R4 IBM) file to run tests against.

    File produced by this code was checked in SeiSee, RadExPro, and Prism 2.
    It is opened and interpreted as intended by all three of these programs.

    """

    path = str(tmp_path_factory.mktemp('manual') / 'test_segy.sgy')

    with open(path, 'bw') as sgy:
        # empty TFH
        sgy.write(bytes(3200))

        # same BFH
        bfh = bytearray(400)
        bfh[0:4] = struct.pack('>i', 666)  # job id
        bfh[16:18] = struct.pack('>h', 500)  # sample interval in microseconds
        bfh[20:22] = struct.pack('>h', 512)  # number of samples per trace
        bfh[24:26] = struct.pack('>h', 1)  # sample format code
        sgy.write(bfh)

        # same trace headers
        tr_hdr = bytearray(240)
        tr_hdr[8:12] = struct.pack('>i', 375)  # FFID - original field record number
        tr_hdr[68:70] = struct.pack('>h', -100)  # ELEVSC - scalar to apply to all elevations
        tr_hdr[70:72] = struct.pack('>h', -100)  # COORDSC - scalar to apply to all coordinates
        tr_hdr[72:76] = struct.pack('>i', 50 * 100)  # SOU_X, with scalar applied
        tr_hdr[76:80] = struct.pack('>i', 75 * 100)  # SOU_Y, with scalar applied
        tr_hdr[84:88] = struct.pack('>i', -1 * 100)  # REC_Y, with scalar applied
        tr_hdr[114:116] = struct.pack('>h', 512)  # NUMSMP - number of samples in a trace
        tr_hdr[116:118] = struct.pack('>h', 500)  # DT - sample interval for this trace in microseconds
        tr_hdr[156:158] = struct.pack('>h', 1984)  # YEAR
        tr_hdr[160:162] = struct.pack('>h', 10)  # HOUR
        tr_hdr[162:164] = struct.pack('>h', 51)  # MINUTE
        tr_hdr[184:188] = struct.pack('>i', 37 * 100)  # CDP_Y, with scalar applied

        for i in range(24):
            tr_hdr[0:4] = struct.pack('>i', i + 1)  # trace number within a line
            tr_hdr[4:8] = struct.pack('>i', i + 1)  # trace number within a file
            tr_hdr[80:84] = struct.pack('>i', i * 2 * 100)  # REC_X, with scalar applied
            tr_hdr[180:184] = struct.pack('>i', int((50 + i * 2) / 2 * 100))  # CDP_X, with scalar applied
            sgy.write(tr_hdr)

            # trace is packed using IBM functions from segy.gfunc
            tr_val = np.ones(512, dtype=np.float32) + i * 3
            tr_bytes = gfunc.pack_ibm32_series(tr_val, '>')
            sgy.write(tr_bytes)

    return path


@pytest.fixture
def geometry():
    """ Return a hand-crafted Geometry object. """

    table = pd.DataFrame(index=range(24), columns=const.THCOLS)

    # elevations
    table.loc[:, 'REC_ELEV'] = 100
    table.loc[:, 'SOU_ELEV'] = 200
    table.loc[:, 'DEPTH'] = 300
    table.loc[:, 'REC_DATUM'] = 400
    table.loc[:, 'SOU_DATUM'] = 500
    table.loc[:, 'SOU_H2OD'] = 600
    table.loc[:, 'REC_H2OD'] = 700

    # coordinates
    table.loc[:, 'SOU_X'] = -100
    table.loc[:, 'SOU_Y'] = -100
    table.loc[:, 'REC_X'] = -100
    table.loc[:, 'REC_Y'] = -100
    table.loc[:, 'CDP_X'] = -100
    table.loc[:, 'CDP_Y'] = -100

    table.fillna(0, inplace=True)

    g = Geometry()
    g._df = table

    return g
