""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np

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

    def __repr__(self):
        return f'DataMatrix: {self._m.shape[0]} traces, {self._m.shape[1]} samples, dt={self.dt}'
