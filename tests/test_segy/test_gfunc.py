""" philoseismos: engineering seismologist's toolbox.

This file contains the tests of general functions defined in philoseismos.segy.gfunc package.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.segy import gfunc


def test_get_endiannes(manually_crafted_segy_file, manually_crafted_little_endian_segy_file):
    """ Test the general function for getting endiannes. """

    assert gfunc.get_endiannes(manually_crafted_segy_file) == '>'
    assert gfunc.get_endiannes(manually_crafted_little_endian_segy_file) == '<'
