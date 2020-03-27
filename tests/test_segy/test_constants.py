""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct

from philoseismos.segy import constants as const


def test_bfhfs_total_size():
    """ Test that BFHFS adds up to exactly 400 bytes. """

    assert struct.calcsize('>' + const.BFHFS) == 400
    assert struct.calcsize('<' + const.BFHFS) == 400
