""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """


class Layer:
    """ This object represents a layer for a layered model. """

    def __init__(self, vp, vs, rho, h):
        """ Create a new layer.

        Args:
            vp: P-wave velocity in m/s.
            vs: S-wave velocity in m/s.
            rho: Density in kg/m^3.
            h: Thickness in m.

        """

        self.vp = vp
        self.vs = vs
        self.rho = rho
        self.h = h
