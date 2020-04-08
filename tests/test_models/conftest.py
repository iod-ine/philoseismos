""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest

from philoseismos.models.hlm import HorizontallyLayeredMedium


@pytest.fixture
def hlm():
    """ A basic HorizontallyLayeredMedium. """

    return HorizontallyLayeredMedium(vp=1500, vs=750, rho=2000)
