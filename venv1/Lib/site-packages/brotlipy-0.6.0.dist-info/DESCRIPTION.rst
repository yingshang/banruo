brotlipy
========

This library contains Python bindings for the reference Brotli encoder/decoder,
`available here`_. This allows Python software to use the Brotli compression
algorithm directly from Python code.

To use it simply, try this:

.. code-block:: python

    import brotli
    data = brotli.decompress(compressed_data)

More information can be found `in the documentation`_.

.. _available here: https://github.com/google/brotli
.. _in the documentation: https://brotlipy.readthedocs.org

License
-------

The source code of brotlipy is available under the MIT license. Brotli itself
is made available under the Version 2.0 of the Apache Software License. See the
LICENSE and libbrotli/LICENSE files for more information.

Authors
-------

brotlipy is maintained by Cory Benfield.


Changelog
=========

0.6.0 (2016-09-08)
------------------

- Resolved a bug where ``decompress()`` would return an empty bytestring
  instead of erroring if the provided bytestring was small enough.
- Added the ``finish()`` method to the streaming decompressor.

0.5.1 (2016-08-17)
------------------

- Update to v0.5.2 of the Brotli library.
- Add new exception type (``Error``).
- Add compatiblity with C++ brotli library by aliasing ``Error`` to ``error``.
- Extra error checking of input parameters to the compressor.

0.5.0 (2016-08-16)
------------------

- Update to v0.5.0 of the Brotli library.
- Extend one-shot compression API to include all control parameters.
- Added streaming/incremental compression API.
- Added flags to control compression mode.

0.4.0 (2016-08-01)
------------------

Update to v0.4.0 of the Brotli library.

0.3.0 (2016-05-11)
------------------

Update to v0.3.0 of the Brotli library.

0.2.0 (2015-10-05)
------------------

Fix broken ``brotli.compress`` support on Windows.

0.1.3 (2015-10-05)
------------------

- Added basic for ``brotli.compress`` through a C wrapper included in this
  library.


