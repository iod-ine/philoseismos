""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import math


class Layer:
    """ This object represents a layer for a layered model. """

    def __init__(self, *, vp=None, vs=300, rho=None, h=10, q=None):
        """ Create a new layer.

        Args:
            vp: P-wave velocity in m/s.
            vs: S-wave velocity in m/s.
            rho: Density in kg/m^3.
            h: Thickness in m.

        """

        self.vs = vs
        self.h = h
        self.vp = vp if vp else vs * math.sqrt(3)  # assume that Lame parameters are equal and vp = vs * sqrt(3)
        self.rho = rho if rho else 310 * self.vp ** 0.25  # use the Gardner's relation to compute rho
        self.q = q

    def __repr__(self):
        vp = f'vp={self.vp}' if self.vp == int(self.vp) else f'vp≈{round(self.vp)}'
        vs = f'vs={self.vs}' if self.vs == int(self.vs) else f'vs≈{round(self.vs)}'
        rho = f'rho={self.rho}' if self.rho == int(self.rho) else f'rho≈{round(self.rho)}'
        h = f'h={self.h}' if self.h == round(self.h, 2) else f'h≈{round(self.h, 2)}'
        return f'Layer({vp}, {vs}, {rho}, {h})'
