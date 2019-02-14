Run NURBS-Python (geomdl) from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|RTD|_ |PYPI|_

**geomdl.cli** module provides a set of commands for using `geomdl <https://pypi.org/project/geomdl>`_ library from
the command line.

Installation
============

From PyPI
---------

Installing via `pip <https://pip.pypa.io/en/stable/>`_ is the easiest and the recommended method

.. code-block:: console

    $ pip install geomdl.cli


If you are getting permission errors on Linux, you can use ``--user`` switch to install to current user's package
directory.

.. code-block:: console

    $ pip install --user geomdl.cli

From the repository
-------------------

* Clone the repository: ``git clone https://github.com/orbingol/geomdl-cli.git``
* Inside the directory containing the cloned repository, run: ``pip install .``
* The setup script will install all required dependencies

Using geomdl-cli
================

After the package installation, the command-line application ``geomdl-cli`` will be automatically available. If you are
getting file not found errors, please make sure that Python and its scripts directory is listed under the PATH
environmental variable.

The following structure explains the most basic usage of the command-line application.

``geomdl-cli {command} {options}``

``{command}`` represents the functionality that ``geomdl-cli`` application will be running. Please refer to the list
below for the commands which come with the package by default.

``{options}`` represents the parameters that is being input to the command. Every command comes with a different set of
options. Please refer to the individual command help for more details.

Available commands
------------------

* **help:** displays the package help text, e.g. available commands, how to use them, etc.
* **version:** displays the package version
* **config:** displays the configuration
* **plot:** plots single or multiple NURBS curves and surfaces using Matplotlib
* **eval:** evaluates NURBS shapes and exports the evaluated points in supported formats, e.g. csv, txt and vtk
* **export:** exports NURBS shapes in supported CAD exchange formats

Individual command help
-----------------------

``geomdl-cli {command} --help``

Documentation
=============

https://geomdl-cli.readthedocs.io/

Author
======

* Onur Rauf Bingol (`@orbingol <https://github.com/orbingol>`_)

License
=======

geomdl-cli is licensed under the `MIT License <https://github.com/orbingol/geomdl-cli/blob/master/LICENSE>`_


.. |RTD| image:: https://readthedocs.org/projects/geomdl-cli/badge/?version=latest
.. _RTD: https://geomdl-cli.readthedocs.io/en/latest/?badge=latest

.. |PYPI| image:: https://img.shields.io/pypi/v/geomdl.cli.svg
.. _PYPI: https://pypi.org/project/geomdl.cli/
