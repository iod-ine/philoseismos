""" philoseismos: engineering seismologist's toolbox.

This file defines a TextualFileHeader object.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """


class TextualFileHeader:
    """ This object represents a textual file header of a SEG-Y file. """

    def __init__(self):
        """ Create a new TFH object. """

        self._contents = ' ' * 3200

    @classmethod
    def load(cls, file: str):
        """ Load TFH from file a SEG-Y file.

        Args:
            file (str) : Path to a SEG-Y file to load from.

        """

        tfh = cls()

        with open(file, 'br') as sgy:
            tfh._contents = sgy.read(3200).decode('cp500')

        return tfh

    def __repr__(self):
        return self._contents

    def __str__(self):
        pass
