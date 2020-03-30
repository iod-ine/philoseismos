""" philoseismos: engineering seismologist's toolbox.

This file contains the tests of general functions defined in philoseismos.segy.gfunc package.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import random

from philoseismos.segy import gfunc


# there are 2 types of value getting functions in gfunc: `get_` functions and `grab_` functions.
# `get_` functions are used on file paths, they open and close the file.
# `grab_` functions are used on opened files, they seek the value without closing the file.

# first are the tests for `get_` functions

def test_get_endiannes(manually_crafted_segy_file, manually_crafted_little_endian_segy_file):
    """ Test the general function for getting endiannes. """

    assert gfunc.get_endiannes(manually_crafted_segy_file) == '>'
    assert gfunc.get_endiannes(manually_crafted_little_endian_segy_file) == '<'


def test_get_sample_format_code(manually_crafted_segy_file):
    """ Test the general function for getting sample format code. """

    assert gfunc.get_sample_format_code(manually_crafted_segy_file) == 3


def test_get_sample_format(manually_crafted_segy_file):
    """ Test the general function for getting sample format. """

    assert gfunc.get_sample_format(manually_crafted_segy_file) == (2, 'h', '2-byte signed integer')


def test_get_trace_length(manually_crafted_segy_file):
    """ Test the general function for getting the trace length. """

    assert gfunc.get_trace_length(manually_crafted_segy_file) == 512


def test_get_number_of_traces(manually_crafted_segy_file):
    """ Test the general function for getting number of traces. """

    assert gfunc.get_number_of_traces(manually_crafted_segy_file) == 24


# then are the tests for the `grab_` functions

def test_grab_endiannes(manually_crafted_segy_file, manually_crafted_little_endian_segy_file):
    """ Test the general function for grabbing endiannes. """

    # check that the returned value is correct and the the cursor is
    # returned to the original position after the grab

    with open(manually_crafted_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_endiannes(sgy) == '>'
        assert sgy.tell() == position

    with open(manually_crafted_little_endian_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_endiannes(sgy) == '<'
        assert sgy.tell() == position


def test_grab_sample_format_code(manually_crafted_segy_file):
    """ Test the general function for grabbing sample format code. """

    # check that the returned value is correct and the the cursor is
    # returned to the original position after the grab

    with open(manually_crafted_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_sample_format_code(sgy) == 3
        assert sgy.tell() == position


def test_grab_sample_format(manually_crafted_segy_file):
    """ Test the general function for grabbing sample format. """

    # check that the returned value is correct and the the cursor is
    # returned to the original position after the grab

    with open(manually_crafted_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_sample_format(sgy) == (2, 'h', '2-byte signed integer')
        assert sgy.tell() == position


def test_grab_trace_length(manually_crafted_segy_file):
    """ Test the general function for grabbing trace length. """

    # check that the returned value is correct and the the cursor is
    # returned to the original position after the grab

    with open(manually_crafted_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_trace_length(sgy) == 512
        assert sgy.tell() == position


def test_grab_number_of_traces(manually_crafted_segy_file):
    """ Test the general function grabbing number of traces. """

    # check that the returned value is correct and the the cursor is
    # returned to the original position after the grab

    with open(manually_crafted_segy_file, 'br') as sgy:
        sgy.seek(random.randint(0, 3600))
        position = sgy.tell()
        assert gfunc.grab_number_of_traces(sgy) == 24
        assert sgy.tell() == position
