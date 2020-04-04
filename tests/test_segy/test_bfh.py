""" philoseismos: engineering seismologist's toolbox.

This file contains tests for the BinaryFileHeader object.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest

from philoseismos.segy.bfh import BinaryFileHeader


def test_creating_new_bfhs():
    """ Test the creating of BFHs. """

    bfh = BinaryFileHeader()

    # it should be a BFH, where all values are set to 0
    assert bfh['job_id'] == 0
    assert bfh['sample_interval'] == 0
    assert bfh['samples_per_trace'] == 0
    assert bfh['sample_format'] == 0


def test_setting_values():
    """ Test that BFHs allow setting values using dict-like syntax. """

    bfh = BinaryFileHeader()

    bfh['job_id'] = 666
    assert bfh['job_id'] == 666

    # all the values in the BFH are integers, setting it to non-integer should raise an error
    with pytest.raises(ValueError):
        bfh['job_id'] = 11.73

    # keys that are not in the BFH should raise an error
    with pytest.raises(ValueError):
        bfh['random_key'] = 9


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that BFH object loads from file correctly. """

    # to load the BFH from a SEG-Y file, use a .load() method
    bfh = BinaryFileHeader.load(manually_crafted_segy_file)

    # BFH should behave like a dictionary for getting the individual values
    assert bfh['job_id'] == 666
    assert bfh['sample_interval'] == 500
    assert bfh['samples_per_trace'] == 512
    assert bfh['sample_format'] == 3
