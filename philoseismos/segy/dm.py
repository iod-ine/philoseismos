""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np
import scipy.fftpack as fft

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

    def dispersion_image(self, c_max, c_min=1, c_step=1, f_max=150):
        """ Compute the dispersion image for the traces.

        Make sure that the OFFSET header in the Geometry is filled correctly!

        Args:
            c_max: Maximum phase velocity to include.
            c_min: Minimum phase velocity to include.
            c_step: Step for the phase velocities.
            f_max: Maximum frequency to consider. Defaults to 150 Hz.

        Returns:
            V: A 2D array (phase velocity, frequency) that contains values for the dispersion image.

        Notes:
            The algorithm used to calculate the dispersion image is described in Park et al. - 1998 -
            Imaging dispersion curves of surface waves on multi-channel record.
            Extent of the returned image will be [0, f_max, 1, c_max]

        """

        U = fft.fft(self._m)
        f = fft.fftfreq(n=U.shape[1], d=self.dt / 1e6)

        U, f = U[:, f >= 0], f[f >= 0]
        U, f = U[:, f <= f_max], f[f <= f_max]

        P = np.angle(U)
        ws = 2 * np.pi * f
        cs = np.arange(c_min, c_max + c_step, c_step)
        xs = self._headers.OFFSET.values

        V = np.empty(shape=(cs.size, f.size), dtype=complex)

        for i, w in enumerate(ws):
            for j, c in enumerate(cs):
                _v = np.exp(1j * (w * xs / c + P[:, i]))
                V[cs.size - 1 - j, i] = _v.sum()

        return V
