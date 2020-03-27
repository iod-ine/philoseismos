""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.segy.bfh import BinaryFileHeader


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that BFH object loads from file correctly. """

    # to load the BFH from a SEG-Y file, use a .load() method
    bfh = BinaryFileHeader.load(manually_crafted_segy_file)

    # BFH should behave like a dictionary for getting the individual values
    assert bfh['job_id'] == 666
    assert bfh['sample_interval'] == 500
    assert bfh['samples_per_trace'] == 512
    assert bfh['sample_format'] == 3
