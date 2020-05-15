""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
import pandas as pd


class RayleighDispersionCurve:

    def __init__(self):
        """ Create a new Rayleigh Dispersion Image. """

        self.freqs = None
        self.modal_curves = []

    @classmethod
    def load_from_rdcscalc(cls, file):
        """ Load the DCs generated with rdcscalc program. """

        curves = pd.read_csv(file)

        out = cls()

        out.modal_curves = [curves['Fundamental']]
        out.modal_curves.append(curves['1st'])
        out.modal_curves.append(curves['2nd'])
        out.modal_curves.append(curves['3rd'])
        out.modal_curves.append(curves['4th'])
        out.modal_curves.append(curves['5th'])

        out.freqs = np.arange(0, 1500, 1) * 0.1 + 0.1

        return out

    @classmethod
    def load_from_radex(cls, file):
        """ Load the DCs exported from RadExPro's MASW module. """

        with open(file, 'r') as cur:
            cur.readline()  # skip first 2 lines
            cur.readline()

            out = cls()
            out.freqs = []

            n = int(cur.readline())  # number of points in fundamental curve

            fs = np.empty(n)
            cs = np.empty(n)

            for i in range(n):
                f, c = map(float, cur.readline().split())
                fs[i] = f
                cs[i] = c

            out.freqs.append(fs)
            out.modal_curves.append(cs)

            k = int(cur.readline())  # number of additional curves

            for i in range(k):
                cur.readline()
                n = int(cur.readline())  # number of points in the curve

                fs = np.empty(n)
                cs = np.empty(n)

                for i in range(n):
                    f, c = map(float, cur.readline().split())
                    fs[i] = f
                    cs[i] = c

                out.freqs.append(fs)
                out.modal_curves.append(cs)

        return out

    def export_modal_curves_for_radex(self, filename, *, sou_x=500, rec_x_0, rec_x_1):
        """ Export modal curves to a text file accepted by MASW module in RadExPro. """

        fundamental = ''
        count = 0
        for f, c in zip(self.freqs, self.modal_curves[0]):
            if not np.isnan(c):
                fundamental += f'{f}\t{c}\n'
                count += 1
        fundamental = f'True\n{count}\n' + fundamental

        higher = []
        for curve in self.modal_curves[1:]:
            string = ''
            count = 0
            for f, c in zip(self.freqs, curve):
                if not np.isnan(c):
                    string += f'{f}\t{c}\n'
                    count += 1
            string = f'True\n{count}\n' + string
            higher.append(string)

        with open(filename, 'w') as txt:
            txt.write(f'{sou_x} {rec_x_0} {rec_x_1}\n')  # geometry of the survey
            txt.write(fundamental)

            txt.write(f'{len(higher)}\n')  # how many additional modal curves are in the file?
            txt.write(''.join(higher))
