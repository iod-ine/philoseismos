""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np
import pandas as pd

from philoseismos.segy.tfh import TextualFileHeader
from philoseismos.segy.bfh import BinaryFileHeader
from philoseismos.segy.g import Geometry
from philoseismos.segy.dm import DataMatrix

from philoseismos.segy import gfunc
from philoseismos.segy import constants as const


class SegY:
    """ This object represents a SEG-Y file. """

    def __init__(self):
        self.tfh = TextualFileHeader()
        self.bfh = BinaryFileHeader()
        self.g = Geometry()
        self.dm = DataMatrix()

        self.file = None

    @classmethod
    def load(cls, file: str):
        """ Load the SEG-Y file. """

        segy = cls()

        with open(file, 'br') as sgy:
            endian = gfunc.grab_endiannes(sgy)
            sfc = gfunc.grab_sample_format_code(sgy)
            nt = gfunc.grab_number_of_traces(sgy)
            tl = gfunc.grab_trace_length(sgy)
            si = gfunc.grab_sample_interval(sgy)
            ss, fl, _ = const.SFC[sfc]
            dtype = const.DTYPEMAP[sfc]

            raw_tfh = sgy.read(3200)
            raw_bfh = sgy.read(400)

            header_data = np.empty(shape=(nt, 90), dtype=np.int32)
            segy.dm._m = np.empty(shape=(nt, tl), dtype=dtype)

            if sfc == 1:  # IBM is a special case
                pass
            else:
                trace_fs = endian + fl * tl

                for i in range(nt):
                    raw_header = sgy.read(240)
                    header = struct.unpack(endian + const.THFS, raw_header[:232])
                    header_data[i] = header

                    raw_trace = sgy.read(ss * tl)
                    trace_values = struct.unpack(trace_fs, raw_trace)
                    segy.dm._m[i] = trace_values

        segy.tfh._contents = raw_tfh.decode('cp500')

        bfh_values = struct.unpack(endian + const.BFHFS, raw_bfh)
        segy.bfh._dict = dict(zip(const.BFHCOLS, bfh_values))

        segy.g._df = pd.DataFrame(header_data, index=range(nt), columns=const.THCOLS)
        segy.g._apply_scalars_after_unpacking()

        segy.dm.dt = si
        segy.dm.t = np.arange(0, si * tl / 1000, si / 1000)

        segy.file = file.split('/')[-1]

        return segy

    @classmethod
    def from_matrix(cls, matrix, sample_interval=500):
        """ Create a SegY object from a matrix.

        Args:
            matrix: A numpy matrix where each row is a trace and each column is a sample.
            sample_interval (int): Sample interval in microseconds.

        Notes:
            The needed sample format is detected from the matrix's dtype property.

        """

        segy = cls()

        segy.dm._m = matrix
        segy.dm.dt = sample_interval
        segy.dm.t = np.arange(0, sample_interval * matrix.shape[1] / 1000, sample_interval / 1000)

        segy.bfh['sample_format'] = const.IDTYPEMAP[matrix.dtype.name]
        segy.bfh['sample_interval'] = sample_interval
        segy.bfh['samples_per_trace'] = matrix.shape[1]
        segy.bfh['measurement_system'] = 1
        segy.bfh['byte_offset_of_data'] = 3600
        segy.bfh['no_traces'] = matrix.shape[0]

        segy.g._df = pd.DataFrame(index=range(matrix.shape[0]), columns=const.THCOLS)
        segy.g.loc[:, 'TRACENO'] = np.arange(1, matrix.shape[0] + 1, 1)
        segy.g.loc[:, 'FFID'] = 1
        segy.g.loc[:, 'CHAN'] = np.arange(1, matrix.shape[0] + 1, 1)
        segy.g.loc[:, 'ELEVSC'] = -100
        segy.g.loc[:, 'COORDSC'] = -100
        segy.g.loc[:, 'NUMSMP'] = matrix.shape[1]
        segy.g.loc[:, 'DT'] = sample_interval

        return segy
