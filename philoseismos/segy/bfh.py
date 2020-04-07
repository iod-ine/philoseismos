""" philoseismos: engineering seismologist's toolbox.

This file defines the BinaryFileHeader object - a dictionary-like representation of a SEG-Y
binary file header.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
from collections import OrderedDict

from philoseismos.segy import gfunc
from philoseismos.segy import constants as const


class BinaryFileHeader:
    """ This object represents a binary file header of a SEG-Y file. """

    def __init__(self):
        """ Create a new BFH object. """

        self._dict = OrderedDict(zip(const.BFHCOLS, [0] * 111))

    @classmethod
    def load(cls, file: str):
        """ Load BFH from a SEG-Y file.

        Args:
            file (str) : Path to the SEG-Y file to load from.

        """

        bfh = cls()

        with open(file, 'br') as sgy:
            # get the endian
            endian = gfunc.grab_endiannes(sgy)

            # skip the TFH, read the BFH bytes
            sgy.seek(3200)
            raw = sgy.read(400)

        # unpack and store the values
        values = struct.unpack(endian + const.BFHFS, raw)
        bfh._dict = dict(zip(const.BFHCOLS, values))

        return bfh

    def __repr__(self):
        out = ''
        for k, v in filter(lambda x: x[1] != 0, self._dict.items()):
            out += f'{k:<25}{v:>5}\n'
        return out

    def __getitem__(self, key):
        return self._dict.get(key)

    def __setitem__(self, key, value):
        if not isinstance(value, int):
            raise ValueError('All the values in the BFH have to be integers.')

        if key not in const.BFHCOLS:
            raise ValueError('That key is not in the BFH values.')

        self._dict[key] = value
