""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from sympy import sin, cos, sqrt, pi, Matrix


def rayleigh_layer_matrix(vp, vs, rho, h, c, f):
    """ Calculate the layer matrix used in Rayleigh dispersion equation.

    Args:
        vp: P-wave velocity in the layer, m/s.
        vs: S-wave velocity in the layer, m/s.
        rho: Density of the layer, kg/m^3.
        h: Thickness of the layer, m.
        c: Phase velocity of the wave, m/s.
        f: Frequency of the wave, Hz.

    """

    w = 2 * pi.evalf() * f
    k = w / c

    r = sqrt((c / vp) ** 2 - 1)
    s = sqrt((c / vs) ** 2 - 1)
    g = 2 * (vs / c) ** 2
    d = g - 1

    P = k * r * h
    Q = k * s * h

    a11 = a44 = g * cos(P) - d * cos(Q)
    a12 = a34 = g * s * sin(Q) if c == vp else d / r * sin(P) + g * s * sin(Q)
    a13 = a24 = -(cos(P) - cos(Q)) / rho
    a14 = (cos(P) - cos(Q)) / rho
    a21 = a43 = g * r * sin(P) if c == vs else g * r * sin(P) + d / s * sin(Q)
    a22 = a33 = -d * cos(P) + g * cos(Q)
    a23 = -r * sin(P) / rho if c == vs else -(r * sin(P) + sin(Q) / s) / rho
    a31 = a42 = rho * g * d * (cos(P) - cos(Q))
    a32 = rho * g ** 2 * s * sin(Q) if c == vp else rho * (d ** 2 / r * sin(P) + g ** 2 * s * sin(Q))
    a41 = -rho * g ** 2 * r * sin(P) if c == vs else -rho * (g ** 2 * r * sin(P) + d ** 2 / s * sin(Q))

    A = Matrix([
        [a11, a12, a13, a14],
        [a21, a22, a23, a24],
        [a31, a32, a33, a34],
        [a41, a42, a43, a44]
    ])

    return A
