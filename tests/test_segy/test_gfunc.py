""" philoseismos: engineering seismologist's toolbox.

This file contains the tests of general functions defined in philoseismos.segy.gfunc package.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.segy import gfunc


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


def test_get_number_of_traces(manually_crafted_segy_file):
    """ Test the general function for getting number of traces. """

    assert gfunc.get_number_of_traces(manually_crafted_segy_file) == 24
