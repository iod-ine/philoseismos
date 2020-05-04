""" philoseismos: with passion for the seismic method.

This file defines Surfer6BinaryGrid class, that reads Surfer 6 Binary Grid data format.

author: ivan dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np


class Surfer6TextGrid:

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
        """ Load the Surfer6TextGrid from the specified file. """

        with open(file, 'r') as f:
            id_ = f.readline().strip()

            # first 4 bytes are ID string identifying a file as Surfer 6 Text Grid
            if id_ != 'DSAA':
                raise ValueError('The specified file is not a Surfer 6 Text grid!')

            out = cls()

            # number of grid lines along the X and Y axes
            out.nx, out.ny = map(int, f.readline().split())

            # minimum and maximum X values of the grid
            out.xlo, out.xhi = map(float, f.readline().split())

            # minimum and maximum Y values of the grid
            out.ylo, out.yhi = map(float, f.readline().split())

            # minimum and maximum Z values of the grid
            out.zlo, out.zhi = map(float, f.readline().split())

            # a matrix to hold the data
            out.dm = np.empty(shape=(out.ny, out.nx), dtype=np.float64)

            # now read the rows. each row has a constant Y coordinate.
            # first row corresponds to ylo, last row corresponds to yhi.
            # within each row Z values are ordered from xlo to xhi

            for row in range(out.ny):
                values = []
                while len(values) < out.nx:
                    values += f.readline().split()

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
