""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np

from philoseismos.dispersion.rayleigh import rayleigh_fundamental_mode
from philoseismos.models.hlm import HorizontallyLayeredMedium


def test_rayleigh_fundamental_mode_on_half_space():
    """ Test the function that calculates fundamental mode for the Rayleigh wave. """

    # when Lame coefficients are equal, vp / vs = sqrt(3)
    # in this case the dispersion equation for the Rayleigh wave solves analytically to
    # c = vs * sqrt(2 - 2 * sqrt(3)), or the in the better-known form c = 0.919 * vs

    # this function checks that the fundamental dispersion curve evaluates to this

    vs = 500

    m = HorizontallyLayeredMedium(vp=vs * np.sqrt(3), vs=vs, rho=2000)

    freqs = [1, 10, 100]
    dc = rayleigh_fundamental_mode(m, freqs)

    assert np.allclose(dc, vs * np.sqrt(2 - 2 / np.sqrt(3)))

    # adding a layer with the same velocity should have no effect on the results
    m.add_layer(vp=vs * np.sqrt(3), vs=vs, rho=2000, h=5)
    dc = rayleigh_fundamental_mode(m, freqs)

    assert np.allclose(dc, vs * np.sqrt(2 - 2 / np.sqrt(3)))
