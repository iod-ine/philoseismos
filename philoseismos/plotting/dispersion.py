""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """


def plot_rdc_into(rdc, ax):
    """ Display the Data Matrix in form of an image.

    Args:
        rdc: RayleighDispersionCurve to plot.
        ax: matplotlib Axes object to draw on.

    """

    for i, curve in enumerate(rdc.modal_curves):
        ax.plot(rdc.freqs, curve, label=i)
