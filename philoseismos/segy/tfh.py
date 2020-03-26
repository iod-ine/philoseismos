""" philoseismos: engineering seismologist's toolbox.

author: Ivan Dubrovin
e-mail: io.dubrovin@icloud.com """


class TextualFileHeader:
    """ This object represents a textual file header of a SEG-Y file. """

    def __init__(self):
        """ Create a new TFH object. """

        self._contents = None

    @classmethod
    def load(cls, file):
        """ Load TFH from file. """

        tfh = cls()

        with open(file, 'br') as f:
            tfh._contents = f.read(3200).decode('cp500')

        return tfh

    def __repr__(self):
        return self._contents

    def __str__(self):
        pass
