""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct

from philoseismos.segy import constants as const


def test_bfhfs_total_size():
    """ Test that BFHFS adds up to exactly 400 bytes. """

    assert struct.calcsize('>' + const.BFHFS) == 400
    assert struct.calcsize('<' + const.BFHFS) == 400


def test_thfs_total_size():
    """ Test that THFS adds up to exactly 232 bytes. """

    assert struct.calcsize('>' + const.THFS) == 232
    assert struct.calcsize('<' + const.THFS) == 232
