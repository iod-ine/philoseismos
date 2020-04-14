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

    hlm.add_layer(vp=600, vs=280, rho=1400, h=10)
    expected = "Layer #0: vp=600 vs=280 rho=1400 h=10\n"
    expected += "Half-space: vp=1500 vs=750 rho=2000"
    assert str(hlm) == expected

    hlm.add_layer(vp=350, vs=120, rho=1000, h=5)
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

    hlm.add_layer(vp=100, vs=50, rho=1000, h=10)
    hlm.add_layer(vp=200, vs=100, rho=1200, h=5)
    hlm.add_layer(vp=300, vs=200, rho=1500, h=15)
    hlm.add_layer(vp=500, vs=250, rho=1600, h=20)

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


def test_get_profiles(hlm):
    """ Test the method for getting parameter profiles to plot. """

    z, vp, vs, rho = hlm.get_profiles()
    assert z == [0, 10]
    assert vp == [1500, 1500]
    assert vs == [750, 750]
    assert rho == [2000, 2000]

    hlm.add_layer(vp=400, vs=200, rho=1500, h=10)
    z, vp, vs, rho = hlm.get_profiles(half_space_depth=20)
    assert z == [0, 10, 10, 30]
    assert vp == [400, 400, 1500, 1500]
    assert vs == [200, 200, 750, 750]

    hlm.add_layer(vp=200, vs=100, rho=1000, h=20)
    z, vp, vs, rho = hlm.get_profiles(half_space_depth=5)
    assert z == [0, 20, 20, 30, 30, 35]
    assert vp == [200, 200, 400, 400, 1500, 1500]
    assert vs == [100, 100, 200, 200, 750, 750]
    assert rho == [1000, 1000, 1500, 1500, 2000, 2000]
