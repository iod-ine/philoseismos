""" philoseismos: engineering seismologist's toolbox.

This file defines general functions used in philoseismos.segy package.

Functions that `get_` values are used with paths to SEG-Y files. They open the file, locate
the value that they are extracting, interpret and return it, closing the file.

Functions that `grab_` values are used with file handlers in 'br' mode. They seek the values
in open files, interpret them and return, leaving the file open.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import math

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


def get_sample_interval(file: str):
    """ Return sample interval of the data in the file. """

    with open(file, 'br') as sgy:
        return grab_sample_interval(sgy)


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

    return int((size - 3600) / (240 + tl * nb))


def grab_sample_interval(opened_file):
    """ Grab sample interval. """

    endian = grab_endiannes(opened_file)

    position = opened_file.tell()
    opened_file.seek(3216)
    si = opened_file.read(2)
    opened_file.seek(position)

    return struct.unpack(endian + 'h', si)[0]


# functions to work with IBM values

def unpack_ibm32(val: bytes, endian: str) -> float:
    """ Unpack bytes containing an IBM floating point value. """

    ibm = struct.unpack(endian + 'L', val)[0]

    sign = ibm >> 31
    exponent = ibm >> 24 & 0b1111111
    fraction = (ibm & 0b111111111111111111111111) / float(pow(2, 24))

    return (1 - 2 * sign) * fraction * pow(16, exponent - 64)


def pack_ibm32(value: float, endian: str) -> bytes:
    """ Pack a floating point value into an IBM floating point. """

    if value == 0:
        return bytearray(4)
    elif abs(value) > 7.2370051459731155e+75:
        raise ValueError('The value is too large to be packed as IBM!')
    elif abs(value) < 5.397605346934028e-79:
        raise ValueError('The value is too small to be packed as IBM!')

    if value < 0:
        sign = 1
        value *= -1
    else:
        sign = 0

    M, E = math.frexp(value)
    f = E / 4
    F = math.ceil(f)
    f_err = F - f
    N = M * pow(2, -4 * f_err)
    F += 64
    N = int(N * pow(2, 24))

    uint = (((sign << 7) | F) << 24) | N

    return struct.pack(endian + 'L', uint)


def unpack_ibm32_series(data: bytes, endian: str) -> tuple:
    """ Unpacks a bytearray containing multiple IBM values. """

    out = []
    for i in range(int(len(data) / 4)):
        out.append(unpack_ibm32(data[i * 4: (i + 1) * 4], endian=endian))

    return tuple(out)


def pack_ibm32_series(values: list, endian: str, ) -> bytearray:
    """ Packs an array of values into a bytearray of IBM 32 packed bytes. """

    out = bytearray(len(values) * 4)
    for i, value in enumerate(values):
        out[i * 4: (i + 1) * 4] = pack_ibm32(value=value, endian=endian)
    return out
