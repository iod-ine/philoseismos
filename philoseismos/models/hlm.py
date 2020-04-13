""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import math

from philoseismos.models.layer import Layer
from philoseismos.dispersion.rdc import RayleighDispersionCurve


class HorizontallyLayeredMedium:
    """ This object represents a horizontally layered medium.

     Horizontally layered medium is a collection of horizontal layers stacked on top of a half-space.
     This object can be used in conjunction with functions from philoseismos.dispersion package
     to calculate dispersion curves for Rayleigh and Love waves.

     """

    def __init__(self, *, vp=None, vs=1000, rho=None):
        """ Create a new HorizontallyLayeredMedium.

        Only accepts keyword arguments. Vp and Rho will be computed automatically if no provided.

        Args:
            vp: P-wave velocity in the half-space in m/s.
            vs: S-wave velocity in a half space in m/s.
            rho: Density of the half-space in kg/m^3.

        """

        self.vs = vs
        self.vp = vp if vp else vs * math.sqrt(3)  # assume that Lame parameters are equal and vp = vs * sqrt(3)
        self.rho = rho if rho else 310 * self.vp ** 0.25  # use the Gardner's relation to compute rho

        self._layers = []

    def add_layer(self, *, vp=None, vs=300, rho=None, h=10):
        """ Add a layer on top of the medium. """

        self._layers.append(Layer(vp=vp, vs=vs, rho=rho, h=h))

    def pop_layer(self, index=-1):
        """ Remove and return layer at index (default last). """

        return self._layers.pop(index)

    def get_profiles(self, half_space_depth=10):
        """ Return profiles of all the parameters to plot.

        Returns:
            z, vp, vs, rho: Matplotlib-ready parameter profiles.

        """

        z = [0]
        vp = []
        vs = []
        rho = []

        for layer in reversed(self._layers):
            z += [z[-1] + layer.h] * 2
            vp += [layer.vp] * 2
            vs += [layer.vs] * 2
            rho += [layer.rho] * 2

        z += [z[-1] + half_space_depth]
        vp += [self.vp] * 2
        vs += [self.vs] * 2
        rho += [self.rho] * 2

        return z, vp, vs, rho

    def rayleigh_dispersion_curve(self, freqs):
        """ Return a new Rayleigh Dispersion Image object for this medium. """

        return RayleighDispersionCurve(self, freqs)

    def __repr__(self):
        vp = f'vp={self.vp}' if self.vp == int(self.vp) else f'vp≈{round(self.vp)}'
        vs = f'vs={self.vs}' if self.vs == int(self.vs) else f'vs≈{round(self.vs)}'
        rho = f'rho={self.rho}' if self.rho == int(self.rho) else f'rho≈{round(self.rho)}'
        return f'HorizontallyLayeredMedium({vp}, {vs}, {rho})'

    def __str__(self):
        out = ''

        for i, l in enumerate(reversed(self._layers)):
            vp = f'vp={l.vp}' if l.vp == int(l.vp) else f'vp≈{round(l.vp)}'
            vs = f'vs={l.vs}' if l.vs == int(l.vs) else f'vs≈{round(l.vs)}'
            rho = f'rho={l.rho}' if l.rho == int(l.rho) else f'rho≈{round(l.rho)}'
            h = f'h={l.h}' if l.h == round(l.h, 2) else f'h≈{round(l.h, 2)}'
            out += f'Layer #{i}: {vp} {vs} {rho} {h}\n'

        vp = f'vp={self.vp}' if self.vp == int(self.vp) else f'vp≈{round(self.vp)}'
        vs = f'vs={self.vs}' if self.vs == int(self.vs) else f'vs≈{round(self.vs)}'
        rho = f'rho={self.rho}' if self.rho == int(self.rho) else f'rho≈{round(self.rho)}'
        out += f'Half-space: {vp} {vs} {rho}'
        return out
