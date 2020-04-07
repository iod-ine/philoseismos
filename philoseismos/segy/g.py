""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import struct
import numpy as np
import pandas as pd

from philoseismos.segy import gfunc
from philoseismos.segy import constants as const


class Geometry:
    """ This object represents trace headers of a SEG-Y file. """

    def __init__(self):
        self._df = None

    @classmethod
    def load(cls, file: str):
        """ Load the Geometry from a SEG-Y file. """

        g = cls()

        with open(file, 'br') as sgy:
            # grab endian, number of traces, sample size, and trace length
            endian = gfunc.grab_endiannes(sgy)
            nt = gfunc.grab_number_of_traces(sgy)
            ss = gfunc.grab_sample_format(sgy)[0]
            tl = gfunc.grab_trace_length(sgy)

            # skip TFH and BFH
            sgy.seek(3600)

            # create a matrix to store trace headers' values
            data = np.empty(shape=(nt, 90), dtype=np.int32)

            for i in range(nt):
                # read in, unpack and store the header
                raw_header = sgy.read(240)
                header = struct.unpack(endian + const.THFS, raw_header[:232])
                data[i] = header

                # skip to the next header - one trace worth of bytes
                sgy.seek(sgy.tell() + ss * tl)

        # transform the matrix into a DataFrame
        g._df = pd.DataFrame(data, index=range(nt), columns=const.THCOLS)

        # apply scalars to elevations and coordinates
        g._apply_scalars_after_unpacking()

        return g

    @property
    def loc(self):
        return self._df.loc

    def _apply_scalars_after_unpacking(self):
        """ Apply elevation and coordinate scalars after unpacking. """

        # zero should be treated as one
        self._df.replace({'ELEVSC', 0}, 1, inplace=True)
        self._df.replace({'COORDSC', 0}, 1, inplace=True)

        # take the absolute value of the scalars
        abs_elevsc = abs(self._df.ELEVSC)
        abs_coordsc = abs(self._df.COORDSC)

        # if negative, to be used as a divisor
        neg_elevsc_ind = self._df.ELEVSC < 0
        neg_coordsc_ind = self._df.COORDSC < 0

        self._df.loc[neg_elevsc_ind, 'REC_ELEV'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_ELEV'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'DEPTH'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'REC_DATUM'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_DATUM'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_H2OD'] /= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'REC_H2OD'] /= abs_elevsc

        self._df.loc[neg_coordsc_ind, 'SOU_X'] /= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'SOU_Y'] /= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'REC_X'] /= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'REC_Y'] /= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'CDP_X'] /= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'CDP_Y'] /= abs_coordsc

        # if positive, to be used as a multiplier
        pos_elevsc_ind = self._df.ELEVSC > 0
        pos_coordsc_ind = self._df.COORDSC > 0

        self._df.loc[pos_elevsc_ind, 'REC_ELEV'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_ELEV'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'DEPTH'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'REC_DATUM'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_DATUM'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_H2OD'] *= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'REC_H2OD'] *= abs_elevsc

        self._df.loc[pos_coordsc_ind, 'SOU_X'] *= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'SOU_Y'] *= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'REC_X'] *= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'REC_Y'] *= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'CDP_X'] *= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'CDP_Y'] *= abs_coordsc

    def _apply_scalars_before_packing(self):
        """ Apply elevation and coordinate scalars before packing. """

        # zero should be treated as one
        self._df.replace({'ELEVSC', 0}, 1, inplace=True)
        self._df.replace({'COORDSC', 0}, 1, inplace=True)

        # take the absolute value of the scalars
        abs_elevsc = abs(self._df.ELEVSC)
        abs_coordsc = abs(self._df.COORDSC)

        # for unpacking: if negative, to be used as a divisor
        # so, multiply before packing
        neg_elevsc_ind = self._df.ELEVSC < 0
        neg_coordsc_ind = self._df.COORDSC < 0

        self._df.loc[neg_elevsc_ind, 'REC_ELEV'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_ELEV'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'DEPTH'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'REC_DATUM'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_DATUM'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'SOU_H2OD'] *= abs_elevsc
        self._df.loc[neg_elevsc_ind, 'REC_H2OD'] *= abs_elevsc

        self._df.loc[neg_coordsc_ind, 'SOU_X'] *= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'SOU_Y'] *= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'REC_X'] *= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'REC_Y'] *= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'CDP_X'] *= abs_coordsc
        self._df.loc[neg_coordsc_ind, 'CDP_Y'] *= abs_coordsc

        # for unpacking: if positive, to be used as a multiplier
        # so, divide before packing
        pos_elevsc_ind = self._df.ELEVSC > 0
        pos_coordsc_ind = self._df.COORDSC > 0

        self._df.loc[pos_elevsc_ind, 'REC_ELEV'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_ELEV'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'DEPTH'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'REC_DATUM'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_DATUM'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'SOU_H2OD'] /= abs_elevsc
        self._df.loc[pos_elevsc_ind, 'REC_H2OD'] /= abs_elevsc

        self._df.loc[pos_coordsc_ind, 'SOU_X'] /= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'SOU_Y'] /= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'REC_X'] /= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'REC_Y'] /= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'CDP_X'] /= abs_coordsc
        self._df.loc[pos_coordsc_ind, 'CDP_Y'] /= abs_coordsc
