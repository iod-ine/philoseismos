""" philoseismos: engineering seismologist's toolbox.

This file defines general functions used in philoseismos.segy package.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct


def get_endiannes(file: str):
    """ Return the endiannes of the SEG-Y file.

    Args:
        file (str) : Path to the file.

    """

    # try to read and unpack the sample format code bytes.
    # the value should be between 1 and 16

    with open(file, 'br') as sgy:
        sgy.seek(3224)
        sf = sgy.read(2)

    return '>' if 1 <= struct.unpack('>h', sf)[0] <= 16 else '<'
