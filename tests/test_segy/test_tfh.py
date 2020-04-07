""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """

from philoseismos.segy.tfh import TextualFileHeader


def test_loading_from_file(manually_crafted_segy_file):
    """ Test that TFH object loads from file correctly. """

    # to load the TFH from a SEG-Y file, use a .load() method
    tfh = TextualFileHeader.load(manually_crafted_segy_file)

    # the contents of the TFH are accessed via its repr()
    # check that it's contents are what they should be
    assert repr(tfh)[0:800] == ' ' * 800
    assert repr(tfh)[800:880] == 'Alle warten auf das Licht'.ljust(80)
    assert repr(tfh)[880:960] == 'fürchtet euch fürchtet euch nicht'.ljust(80)
    assert repr(tfh)[960:1040] == 'die Sonne scheint mir aus den Augen'.ljust(80)
    assert repr(tfh)[1040:1120] == 'sie wird heut Nacht nicht untergehen'.ljust(80)
    assert repr(tfh)[1120:1200] == 'und die Welt zählt laut bis zehn'.ljust(80)
    assert repr(tfh)[1200:1280] == 'Eins'.ljust(80)
    assert repr(tfh)[1280:1360] == 'Hier kommt die Sonne'.ljust(80)
    assert repr(tfh)[1360:] == ' ' * 1840


def test_replacing_in_file():
    pass


def test_exporting_to_txt():
    pass


def test_importing_from_txt():
    pass
