Binary File Header
==================
Binary file header contains binary values relevant to the whole SEG-Y file.
Most important values that are stored in the BFH (without them the file can't be read in correctly) are
sample format and sample interval.


A binary file header (BFH) is represented by a ``BinaryFileHeader`` object. It can be imported from
``philoseismos.segy`` sub-package.

Reading BFHs from files
-----------------------

Just like with TFHs, there is more than one way to create a ``BinaryFileHeader`` object from a file:

- ``BinaryFileHeader.load("path/to/file.sgy")`` for loading from SEG-Y files. It takes a path to the file in
  form of a string and returns a BFH object.


Contents of a BFH
-----------------

BFH is a *dictionary-like* object, so it can be used in a following way:

.. code-block:: python

    job_id = bfh['job_id']

Most important keys are:

- ``sample_interval``, the discretization step in micro- or picoseconds
- ``samples_per_trace``, number of samples in each trace
- ``sample_format``, the format used for storing traces (i.e. unsigned integer, float, etc.)
