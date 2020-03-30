""" philoseismos: engineering seismologist's toolbox.

This file defines general functions used in philoseismos.segy package.

Functions that `get_` values are used with paths to SEG-Y files. They open the file, locate
the value that they are extracting, interpret and return it, closing the file.

Functions that `grab_` values are used with file handlers in 'br' mode. They seek the values
in open files, interpret them and return, leaving the file open.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct

from philoseismos.segy.constants import SFC


def get_endiannes(file: str):
    """ Return the endiannes of the SEG-Y file.

    Args:
        file (str) : Path to the file.

    Returns:
        '>' or '<' for big and little endian respectively.

    """

    # try to read and unpack the sample format code bytes.
    # the value should be between 1 and 16

    with open(file, 'br') as sgy:
        sgy.seek(3224)
        sf = sgy.read(2)

    return '>' if 1 <= struct.unpack('>h', sf)[0] <= 16 else '<'


def get_sample_format_code(file: str):
    """ Return the sample format code of the SEG-Y file.

    Args:
        file (str) : Path to the SEG-Y file.

    Returns:
        sfc : Sample format code.

    """

    with open(file, 'br') as sgy:
        sgy.seek(3224)
        sf = sgy.read(2)

    # unpack using big-endian. if it is not in [1, 16],
    # return the little-endian instead

    sfc = struct.unpack('>h', sf)[0]

    return sfc if 1 <= sfc <= 16 else struct.unpack('<h', sf)[0]


def get_sample_format(file: str):
    """ Return the sample format tuple.

    Args:
        file (str) : Path to the SEG-Y file.

    Returns:
        nb : Number of bytes for encoding 1 sample.
        fl : Format letter used to pack / unpack with struct.
        desc : Description of the format.

    """

    sfc = get_sample_format_code(file)

    return SFC[sfc]


def get_trace_length(file: str):
    """ Return the length of the traces in the file (in samples).

    Args:
        file (str) : Path to the SEG-Y file.
    Returns:
        tl : Trace length in samples.

    """

    with open(file, 'br') as sgy:
        endian = grab_endiannes(sgy)
        sgy.seek(3220)
        tl = sgy.read(2)

    return struct.unpack(endian + 'h', tl)[0]


def get_number_of_traces(file: str):
    """ Return number of traces in the file.

    Returned number of traces is calculated from sample format and file size.

    Args:
        file (str) : Path to the SEG-Y file.

    Returns:
        n : Number of traces in the file.

    """

    with open(file, 'br') as sgy:
        return grab_number_of_traces(sgy)


def grab_endiannes(opened_file):
    """ Grab endiannes of the file. """

    position = opened_file.tell()
    opened_file.seek(3224)
    sf = opened_file.read(2)
    opened_file.seek(position)

    return '>' if 1 <= struct.unpack('>h', sf)[0] <= 16 else '<'


def grab_sample_format_code(opened_file):
    """ Grab sample format code. """

    endian = grab_endiannes(opened_file)

    position = opened_file.tell()
    opened_file.seek(3224)
    sf = opened_file.read(2)
    opened_file.seek(position)

    return struct.unpack(endian + 'h', sf)[0]


def grab_sample_format(opened_file):
    """ Grab sample format. """

    sfc = grab_sample_format_code(opened_file)

    return SFC[sfc]


def grab_trace_length(opened_file):
    """ Grab trace length. """

    endian = grab_endiannes(opened_file)

    position = opened_file.tell()
    opened_file.seek(3220)
    tl = opened_file.read(2)
    opened_file.seek(position)

    return struct.unpack(endian + 'h', tl)[0]


def grab_number_of_traces(opened_file):
    """ Grab number of traces. """

    tl = grab_trace_length(opened_file)
    nb = grab_sample_format(opened_file)[0]

    position = opened_file.tell()
    opened_file.seek(0, 2)
    size = opened_file.tell()
    opened_file.seek(position)

    return (size - 3600) / (240 + tl * nb)
