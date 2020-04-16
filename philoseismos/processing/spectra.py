""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
from scipy import fftpack as fft


def average_spectrum(seismogram, dt):
    """ Calculate the average amplitude spectrum of all traces in a seismogram.

    Args:
        seismogram: A matrix where each row is a trace and each column is a sample.
        dt: Sample interval in microseconds.

    Returns:
        freq : The frequency axis.
        amps : The average amplitude spectrum.

    """

    spectrum = np.abs(fft.fft(seismogram))
    avg_spectrum = np.average(spectrum, axis=0)
    freq = fft.fftfreq(avg_spectrum.size, d=dt / 1e6)

    # only return a half of the spectrum (0 Hz to Nyquist frequency)
    avg_spectrum = avg_spectrum[freq > 0]
    freq = freq[freq > 0]

    return freq, avg_spectrum


def average_spectrum_of_dm(data_matrix):
    """ Calculate the average amplitude spectrum of all traces in a Data Matrix.

    Returns:
        freq : The frequency axis.
        amps : The average amplitude spectrum.

    """

    return average_spectrum(data_matrix._m, data_matrix.dt)


def dispersion_image_of_dm(data_matrix, c_max=1200, c_min=1, c_step=1, f_max=150):
    """ Compute the dispersion image for the Data Matrix.

        Make sure that the OFFSET header in the Geometry is filled correctly!

        Args:
            data_matrix: A Data Matrix object.
            c_max: Maximum phase velocity to include.
            c_min: Minimum phase velocity to include.
            c_step: Step for the phase velocities.
            f_max: Maximum frequency to consider. Defaults to 150 Hz.

        Returns:
            V: A 2D array (phase velocity, frequency) that contains values of the dispersion image.

        Notes:
            The algorithm used to calculate the dispersion image is described in Park et al. - 1998 -
            Imaging dispersion curves of surface waves on multi-channel record.
            Extent of the returned image will be [0, f_max, 1, c_max]

    """

    U = fft.fft(data_matrix._m)
    f = fft.fftfreq(n=U.shape[1], d=data_matrix.dt / 1e6)

    U, f = U[:, f >= 0], f[f >= 0]
    U, f = U[:, f <= f_max], f[f <= f_max]

    P = np.angle(U)
    ws = 2 * np.pi * f
    cs = np.arange(c_min, c_max + c_step, c_step)
    xs = np.abs(data_matrix._headers.OFFSET.values)

    V = np.empty(shape=(cs.size, f.size), dtype=complex)

    for i, w in enumerate(ws):
        for j, c in enumerate(cs):
            _v = np.exp(1j * (w * xs / c + P[:, i]))
            V[cs.size - 1 - j, i] = _v.sum()

    return V
