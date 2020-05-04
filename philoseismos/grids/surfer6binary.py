""" philoseismos: with passion for the seismic method.

This file defines Surfer6BinaryGrid class, that reads Surfer 6 Binary Grid data format.

author: ivan dubrovin
e-mail: io.dubrovin@icloud.com """

import struct

import numpy as np


class Surfer6BinaryGrid:

    def __init__(self):
        """ """

        self.nx = None
        self.ny = None
        self.xlo = None
        self.xhi = None
        self.ylo = None
        self.yhi = None
        self.zlo = None
        self.zhi = None

        self.dm = None

    @classmethod
    def load(cls, file):
        """ Load the Surfer6BinaryGrid from the specified file. """

        with open(file, 'br') as f:
            id_ = f.read(4)

            # first 4 bytes are ID string identifying a file as Surfer 6 Binary Grid
            if id_ != b'DSBB':
                raise ValueError('The specified file is not a Surfer 6 Binary grid!')

            out = cls()

            out.nx = struct.unpack('<h', f.read(2))[0]  # number of grid lines along the X axis
            out.ny = struct.unpack('<h', f.read(2))[0]  # number of grid lines along the Y axis
            out.xlo = struct.unpack('<d', f.read(8))[0]  # minimum X value of the grid
            out.xhi = struct.unpack('<d', f.read(8))[0]  # maximum X value of the grid
            out.ylo = struct.unpack('<d', f.read(8))[0]  # minimum Y value of the grid
            out.yhi = struct.unpack('<d', f.read(8))[0]  # maximum Y value of the grid
            out.zlo = struct.unpack('<d', f.read(8))[0]  # minimum Z value of the grid
            out.zhi = struct.unpack('<d', f.read(8))[0]  # maximum Z value of the grid

            # a matrix to hold the data
            out.dm = np.empty(shape=(out.ny, out.nx), dtype=np.float64)

            # now read the rows. each row has a constant Y coordinate.
            # first row corresponds to ylo, last row corresponds to yhi.
            # within each row Z values are ordered from xlo to xhi

            format_string = '<' + 'f' * out.nx

            for row in range(out.ny):
                bytes_ = f.read(out.nx * 4)
                values = struct.unpack(format_string, bytes_)
                out.dm[row, :] = values

        return out

    def invert_yaxis(self):
        """ Inverts the Y axis in the DataMatrix. """

        self.dm = self.dm[::-1, :]
        self.ylo, self.yhi = self.yhi, self.ylo

    def invert_xaxis(self):
        """ Inverts the X axis in the DataMatrix. """

        self.dm = self.dm[:, ::-1]
        self.xlo, self.xhi = self.xhi, self.xlo

    @property
    def extent(self):
        return [self.xlo, self.xhi, self.yhi, self.ylo]
