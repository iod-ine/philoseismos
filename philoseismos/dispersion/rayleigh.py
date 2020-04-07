""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from sympy import sin, cos, sqrt, pi, Matrix, sign, nan
from scipy import optimize


def rayleigh_layer_matrix(layer, c, f):
    """ Calculate the layer matrix used in Rayleigh dispersion equation.

    Args:
        layer: The layer.
        c: Phase velocity of the wave, m/s.
        f: Frequency of the wave, Hz.

    """

    vp = layer.vp
    vs = layer.vs
    rho = layer.rho
    h = layer.h

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


def rayleigh_matrix_for_stack_of_layers(stack_of_layers, c, f):
    """ Calculate the matrix for stack of layers used for Rayleigh dispersion function.

     Args:
         stack_of_layers (list): Stack of layers, like in HLM.
         c: Phase velocity, m/s.
         f: Frequency, Hz.

     """

    A = Matrix.eye(4)

    for layer in stack_of_layers:
        A = A * rayleigh_layer_matrix(layer, c, f)

    return A


def rayleigh_dispersion_function(medium, c, f):
    """ Calculate the value of the Rayleigh dispersion function for a given model and trial c and f. """

    A = rayleigh_matrix_for_stack_of_layers(medium._layers, c, f)

    L1 = A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]
    L2 = A[0, 0] * A[2, 1] - A[0, 1] * A[2, 0]
    L3 = A[0, 0] * A[3, 1] - A[0, 1] * A[3, 0]
    L4 = A[1, 0] * A[2, 1] - A[1, 1] * A[2, 0]
    L5 = A[1, 0] * A[3, 1] - A[1, 1] * A[3, 0]
    L6 = A[2, 0] * A[3, 1] - A[2, 1] * A[3, 0]

    r = sqrt(1 - (c / medium.vp) ** 2)
    s = sqrt(1 - (c / medium.vs) ** 2)
    g = 2 * (medium.vs / c) ** 2
    d = g - 1

    H1 = medium.rho * (g ** 2 * r * s - d ** 2)
    H2 = -medium.rho * r
    H3 = H4 = medium.rho * (g * r * s - d)
    H5 = -medium.rho * s
    H6 = 1 - r * s

    return L1 * H1 + L2 * H2 + L3 * H3 + L4 * H4 + L5 * H5 + L6 * H6


def rayleigh_fundamental_mode(medium, freqs):
    """ Calculate the fundamental dispersion curve of the Rayleigh wave for a given medium. """

    roots = []

    for f in freqs:
        guess = min([layer.vs for layer in medium._layers] + [medium.vs]) / 2

        def dispersion_function(c):
            return rayleigh_dispersion_function(medium, c, f)

        sign_ = sign(dispersion_function(guess))

        while guess < max([layer.vs for layer in medium._layers] + [medium.vs]):
            if sign(dispersion_function(guess)) != sign_:
                root = optimize.bisect(dispersion_function, guess - 1, guess)
                roots.append(root)
                break
            else:
                guess += 1
        else:
            roots.append(nan)

    return roots
