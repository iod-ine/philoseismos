Textual File Header
===================

Textual file header is a a human-readable description of a SEG-Y file.
It contains 3200 characters of text (40 lines, 80 characters each) and has no mandatory format.

A textual file header (TFH) is represented by a ``TextualFileHeader`` object. It can be imported from
``philoseismos.segy`` sub-package.

Reading TFHs from files
-----------------------

There is more than one way to create a ``TextualFileHeader`` object from a file:

- ``TextualFileHeader.load("path/to/file.sgy")`` for loading from SEG-Y files. It takes a path to the file in
  form of a string and returns a TFH object.


Contents of a TFH
-----------------

To get the contents of the TFH in form of one string, use ``repr()``.

