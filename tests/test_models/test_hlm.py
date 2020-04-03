""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

import pytest

from philoseismos.models.layer import Layer


def test_hlm_repr(hlm):
    """ Test the __repr__ method of the HorizontallyLayeredMedium. """

    assert repr(hlm) == 'HorizontallyLayeredMedium(vp=1500, vs=750, rho=2000)'


def test_hlm_str(hlm):
    """ Test the __str__ method of the HorizontallyLayeredMedium. """

    expected = "Half-space: vp=1500 vs=750 rho=2000"
    assert str(hlm) == expected

    hlm.add_layer(600, 280, 1400, 10)
    expected = "Layer #0: vp=600 vs=280 rho=1400 h=10\n"
    expected += "Half-space: vp=1500 vs=750 rho=2000"
    assert str(hlm) == expected

    hlm.add_layer(350, 120, 1000, 5)
    expected = "Layer #0: vp=350 vs=120 rho=1000 h=5\n"
    expected += "Layer #1: vp=600 vs=280 rho=1400 h=10\n"
    expected += "Half-space: vp=1500 vs=750 rho=2000"
    assert str(hlm) == expected


def test_add_layer(hlm):
    """ Test the method for adding layers to the HorizontallyLayeredMedium. """

    hlm.add_layer(vp=500, vs=250, rho=1300, h=10)
    assert len(hlm._layers) == 1
    assert isinstance(hlm._layers[0], Layer)

    l = hlm._layers[0]
    assert l.vp == 500
    assert l.vs == 250
    assert l.rho == 1300
    assert l.h == 10


def test_pop_layer(hlm):
    """ Test the method for popping layers to the HorizontallyLayeredMedium. """

    hlm.add_layer(100, 50, 1000, 10)
    hlm.add_layer(200, 100, 1200, 5)
    hlm.add_layer(300, 200, 1500, 15)
    hlm.add_layer(500, 250, 1600, 20)

    assert len(hlm._layers) == 4

    layer = hlm.pop_layer(0)
    assert len(hlm._layers) == 3
    assert layer.vp == 100
    assert layer.vs == 50

    layer = hlm.pop_layer()
    assert len(hlm._layers) == 2
    assert layer.vp == 500
    assert layer.vs == 250


@pytest.mark.skip
def test_export_to_segy_for_tesseral(hlm):
    """ Test the method for exporting models for Tesseral in SEG-Y format. """

    pass
