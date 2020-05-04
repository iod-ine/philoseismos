""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
import pandas as pd


class RayleighDispersionCurve:

    def __init__(self, medium, freqs):
        """ Create a new Rayleigh Dispersion Image. """

        self.medium = medium
        self.freqs = freqs
        self.modal_curves = []

    def load(self, file):
        """ Load the DCs generated with rdcscalc program. """

        curves = pd.read_csv(file)

        self.modal_curves = [curves['Fundamental']]
        self.modal_curves.append(curves['1st'])
        self.modal_curves.append(curves['2nd'])
        self.modal_curves.append(curves['3rd'])
        self.modal_curves.append(curves['4th'])
        self.modal_curves.append(curves['5th'])

        self.freqs = np.arange(0, 500, 1) * 0.1 + 0.1

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
