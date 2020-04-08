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
