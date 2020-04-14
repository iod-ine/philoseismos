""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
from scipy import optimize
from tqdm import tqdm

from philoseismos.dispersion.rayleigh import rayleigh_fundamental_mode, rayleigh_dispersion_function


class RayleighDispersionCurve:

    def __init__(self, medium, freqs):
        """ Create a new Rayleigh Dispersion Image. """

        self.medium = medium
        self.freqs = freqs
        self.modal_curves = []

    def calculate_modal_curves(self, n):
        """ Calculate first n modal dispersion curves. """

        self._calculate_fundamental_mode()

        for i in range(n - 1):
            self._calculate_next_mode()

    def export_modal_curves_for_radex(self, filename, *, sou_x=500, rec_x_0, rec_x_1):
        """ Export modal curves to a text file accepted by MASW module in RadExPro. """

        with open(filename, 'w') as txt:
            txt.write(f'{sou_x} {rec_x_0} {rec_x_1}\n')  # geometry of the survey

            # write the fundamental curve
            txt.write('True\n')  # is this curve displayed on the DI?
            txt.write(f'{len(self.freqs)}\n')  # how many points are in this curve?
            for f, v in zip(self.freqs, self.modal_curves[0]):  # write all freq-val pairs
                txt.write(f'{f}\t{v}\n')

            txt.write(f'{len(self.modal_curves) - 1}\n')  # how many additional modal curves are in the file?

            for curve in self.modal_curves[1:]:  # write the rest of the curves
                txt.write('True\n')
                txt.write(f'{len(curve)}\n')
                for f, v in zip(self.freqs, curve):
                    txt.write(f'{f}\t{v}\n')

    def _calculate_fundamental_mode(self):
        """ Calculate the fundamental Rayleigh mode. """

        fm = rayleigh_fundamental_mode(self.medium, self.freqs)
        self.modal_curves = [fm]

    def _calculate_next_mode(self):
        """ Calculate the next available higher modal curve. """

        if len(self.modal_curves) < 1:
            raise ValueError('Before calculating the higher modes, calculate the fundamental one.')

        max_beta = max([layer.vs for layer in self.medium._layers] + [self.medium.vs])
        roots = []

        for f, c_prev in tqdm(zip(self.freqs, self.modal_curves[-1])):

            if np.isnan(c_prev):
                roots.append(np.nan)
                continue

            guess = c_prev + 0.001

            def dispersion_function(c):
                return rayleigh_dispersion_function(self.medium, c, f)

            sign = np.sign(dispersion_function(guess))

            while guess < max_beta:
                if np.sign(dispersion_function(guess)) != sign:
                    try:
                        root = optimize.bisect(dispersion_function, guess - 1, guess)
                        roots.append(root)
                    except ValueError:
                        roots.append(np.nan)
                    break
                else:
                    guess += 1
            else:
                roots.append(np.nan)

        self.modal_curves.append(roots)
