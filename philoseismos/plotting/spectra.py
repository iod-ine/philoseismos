""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import numpy as np
import scipy.fftpack as fft

from philoseismos.processing.spectra import average_spectrum_of_dm, dispersion_image_of_dm


def plot_average_spectrum_of_dm_into(data_matrix, ax, norm=True, fill=True):
    """ Plot the average spectrum of given DM into given Axes. """

    freq, amps = average_spectrum_of_dm(data_matrix)

    if norm:
        amps /= amps.max()

    return ax.fill_between(freq, amps) if fill else ax.plot(freq, amps)


def imshow_dispersion_image_of_dm_into(data_matrix, ax, c_max=1200, c_min=1, c_step=1, f_max=150):
    """ Plot the dispersion image of given DM into given Axes.

    Args:
        data_matrix: The DataMatrix object.
        ax: matplotlib Axes to plot into.
        c_max: Maximum phase velocity to include.
        c_min: Minimum phase velocity to include.
        c_step: Step for the phase velocities.
        f_max: Maximum frequency to consider. Defaults to 150 Hz.

    Returns:
        The Image object.

    """

    V = dispersion_image_of_dm(data_matrix, c_max, c_min, c_step, f_max)
    image = ax.imshow(np.abs(V), aspect='auto', interpolation='spline36', extent=[0, f_max, c_min, c_max])

    return image


def pcolormesh_fk_spectrum_of_dm_into(data_matrix, ax, f_max=150):
    fft2d = np.abs(fft.fft2(data_matrix._m.T))

    dx = np.diff(data_matrix._headers.OFFSET)[0]
    dt = data_matrix.dt * 1e-6

    kn = 1 / 2 / dx
    fn = 1 / 2 / dt

    ks = np.linspace(-kn, kn, data_matrix._m.shape[0] + 1)
    fs = np.linspace(-fn, fn, data_matrix._m.shape[1] + 1)

    fft2d = fft.fftshift(fft2d)
    fft2d = fft2d[:, ::-1]

    pc = ax.pcolormesh(ks, fs, fft2d, cmap='binary')
    ax.set_ylim(0, f_max)

    return pc
