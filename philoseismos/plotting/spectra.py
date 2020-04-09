""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.processing.spectra import average_spectrum_of_dm


def plot_average_spectrum_of_dm_into(data_matrix, ax):
    """ Plot the average spectrum of given DM into given Axes. """

    freq, amps = average_spectrum_of_dm(data_matrix)
    ax.fill_between(freq, amps)
