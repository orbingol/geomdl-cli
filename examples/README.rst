Example input files to use with geomdl-cli
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This directory contains example input files to use with ``geomdl-cli`` command-line tool.

How to run the examples
=======================

The following command will plot a 2-dimensional NURBS curve in circular shape:

.. code-block:: console

    $ geomdl-cli plot curve2d.yaml

The following command will evaluate the input 3-dimensional curve and export the evaluated points as a .CSV file. The
exported points will be written to ``curve3d.csv`` file

.. code-block:: console

    $ geomdl-cli eval curve3d.yaml --format=csv

The following command will change the evaluation delta to :math:`0.05` and the exported points will be written to
``my_curve.csv`` file.

.. code-block:: console

    $ geomdl-cli eval curve3d.yaml --delta=0.05 --format=csv --name=my_curve.csv

Please refer to the `documentation <https://geomdl-cli.readthedocs.io>`_ for more details.

List of examples
================

* Curve examples: ``curve2d.yaml`` and ``curve3d.yaml``
* Surface examples: ``surface.cfg``, ``surface.yaml`` and ``surface.json``
* Multi-surface examples: ``surface_multi.cfg``, ``surface_multi.json`` and ``surface_decomposed.yaml``
