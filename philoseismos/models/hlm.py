""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.models.layer import Layer
from philoseismos.dispersion.rdc import RayleighDispersionCurve


class HorizontallyLayeredMedium:
    """ This object represents a horizontally layered medium.

     Horizontally layered medium is a collection of horizontal layers stacked on top of a half-space.
     This object can be used in conjunction with functions from philoseismos.dispersion package
     to calculate dispersion curves for Rayleigh and Love waves.

     """

    def __init__(self, vp, vs, rho):
        """ Create a new HorizontallyLayeredMedium.

        Args:
            vp: P-wave velocity in the half-space in m/s.
            vs: S-wave velocity in a half space in m/s.
            rho: Density of the half-space in kg/m^3.

        """

        self.vp = vp
        self.vs = vs
        self.rho = rho

        self._layers = []

    def add_layer(self, vp, vs, rho, h):
        """ Add a layer on top of the medium. """

        self._layers.append(Layer(vp, vs, rho, h))

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
        return f'HorizontallyLayeredMedium(vp={self.vp}, vs={self.vs}, rho={self.rho})'

    def __str__(self):
        out = ''

        for i, l in enumerate(reversed(self._layers)):
            out += f'Layer #{i}: vp={l.vp} vs={l.vs} rho={l.rho} h={l.h}\n'

        out += f'Half-space: vp={self.vp} vs={self.vs} rho={self.rho}'
        return out
