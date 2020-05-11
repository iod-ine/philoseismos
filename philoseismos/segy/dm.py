""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np

from philoseismos.segy.g import Geometry
from philoseismos.segy import gfunc
from philoseismos.segy import constants as const


class DataMatrix:
    """ This object represents traces of the SEG-Y file. """

    def __init__(self):
        self.dt = None
        self.t = None
        self._m = None
        self._headers = None

    @classmethod
    def load(cls, file: str):
        """ Load the DataMatrix from a SEG-Y file. """

        dm = cls()

        with open(file, 'br') as sgy:
            # grab endian, format letter, trace length, sample size, number of traces, data type, and sample interval
            endian = gfunc.grab_endiannes(sgy)
            sfc = gfunc.grab_sample_format_code(sgy)
            tl = gfunc.grab_trace_length(sgy)
            nt = gfunc.grab_number_of_traces(sgy)
            si = gfunc.grab_sample_interval(sgy)

            ss, fl, _ = const.SFC[sfc]
            dtype = const.DTYPEMAP[sfc]

            dm._m = np.empty(shape=(nt, tl), dtype=dtype)

            sgy.seek(3600)

            if sfc == 1:  # IBM is a special case
                pass
            else:
                format_string = endian + fl * tl

                for i in range(nt):
                    sgy.seek(sgy.tell() + 240)  # skip trace header
                    raw_trace = sgy.read(ss * tl)

                    values = struct.unpack(format_string, raw_trace)
                    dm._m[i] = values

        dm.dt = si
        dm.t = np.arange(0, si * tl / 1000, si / 1000)

        return dm

    def extract_by_indices(self, indices):
        """ Return a new DM, constructed from traces extracted by given indices. """

        new = DataMatrix()
        new.dt = self.dt
        new.t = np.copy(self.t)
        new._m = np.copy(self._m[indices])
        new._headers = Geometry()
        new._headers._df = self._headers.loc[indices, :].copy()

        return new

    def filter(self, header, first, last, step):
        """ Return a new DM filtered in a way that header = range(first, last + 1, step).

        Args:
            header (str): Header name to filter by.
            first (float): First value of the header.
            last (float): Last value of the header (inclusive).
            step (float): Step of the header.

        Returns:
            A new DataMatrix object.

        """

        new = DataMatrix()
        new.dt = self.dt
        new.t = np.copy(self.t)

        subset = self._headers._df.loc[self._headers._df[header] >= first]
        subset = subset.loc[subset[header] <= last]
        subset = subset.loc[(subset[header] - first) % step == 0]

        new._m = self._m[subset.index]
        new._headers = Geometry()
        new._headers._df = subset.reset_index().drop('index', axis=1)
        new._headers._df.TRACENO = new._headers._df.index + 1
        new._headers._df.SEQNO = new._headers._df.index + 1

        return new

    def resample(self, dt):
        """ Return a new DM with a bigger dt.

        Args:
            dt: New dt.

        Returns:
            A new DataMatrix object.

        """

        nth = int(dt / self.dt)

        if nth != dt / self.dt:
            raise ValueError(f"Can't transform dt={self.dt} into dt={dt}!")

        new = DataMatrix()
        new.dt = dt
        new.t = self.t[::nth]

        new._m = self._m[:, ::nth]
        new._headers = Geometry()
        new._headers._df = self._headers._df.copy()

        return new

    def crop(self, t, inplace=False):
        """ Return a new DM with new trace length.

        Args:
            t: New trace length.
            inplace (bool): If True, modify this DM instead of returning a new one.

        Returns:
            A new DataMatrix object.

        """

        if inplace:
            self._m = self._m[:, self.t <= t]
            self.t = self.t[self.t <= t]
        else:
            new = DataMatrix()
            new.dt = self.dt
            new.t = self.t[self.t <= t]

            new._m = self._m[:, self.t <= t]
            new._headers = Geometry()
            new._headers._df = self._headers._df.copy()

            return new

    def __repr__(self):
        return f'DataMatrix: {self._m.shape[0]} traces, {self._m.shape[1]} samples, dt={self.dt}'
