""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest
import struct
import numpy as np


@pytest.fixture
def bad_binary_grd_file(tmp_path_factory):
    """ A file without the needed ID string at the beginning."""

    tempdir = tmp_path_factory.mktemp('tempdir')
    file = str(tempdir / 'bad_file.grd')

    with open(file, 'bw') as f:
        bad_data = 'This is very bad data!'.encode(encoding='cp500')
        f.write(bad_data)

    return file


@pytest.fixture
def bad_text_grd_file(tmp_path_factory):
    """ A file without the needed ID string at the beginning."""

    tempdir = tmp_path_factory.mktemp('tempdir')
    file = str(tempdir / 'bad_file.grd')

    with open(file, 'w') as f:
        bad_data = 'This is very bad data!'
        f.write(bad_data)

    return file


@pytest.fixture(scope='module')
def binary_grd_file(tmp_path_factory):
    """ A manually created .grf file to test. """

    tempdir = tmp_path_factory.mktemp('tempdir')
    file = str(tempdir / 'test.grd')

    # pack nx, ny, xlo, xhi, ylo, yhi, zlo, zhi
    format_string = '<hhdddddd'
    values = 10, 15, 0, 9, 10, 38, 0, 150
    packed_header = struct.pack(format_string, *values)

    # create the data to pack
    data = np.arange(150).reshape(15, 10)
    data_format_string = '<' + 'f' * 10

    with open(file, 'bw') as f:
        f.write(b'DSBB')  # id string
        f.write(packed_header)

        for row in data:
            packed = struct.pack(data_format_string, *row)
            f.write(packed)

    return file


@pytest.fixture(scope='module')
def text_grd_file(tmp_path_factory):
    """ A manually created .grf file to test. """

    tempdir = tmp_path_factory.mktemp('tempdir')
    file = str(tempdir / 'test.grd')

    # create the data
    data = np.arange(150).reshape(15, 10)

    with open(file, 'w') as f:
        f.write('DSAA\n')  # id string
        f.write('10 15\n')  # nx and ny
        f.write('0 9\n')  # xlo and xhi
        f.write('10 38\n')  # ylo and yhi
        f.write('0 150\n')  # zlo and zhi

        for row in data:
            f.write(' '.join(map(str, row)))
            f.write('\n')

    return file
