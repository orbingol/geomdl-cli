Run NURBS-Python (geomdl) from the command line
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|RTD|_

``geomdl.cli`` module provides a set of commands for using `geomdl <https://pypi.org/project/geomdl>`_ library from
the command line.

Installation
============

From PyPI
---------

``pip install geomdl.cli``

From the repository
-------------------

* Clone the repository: ``git clone https://github.com/orbingol/geomdl-cli.git``
* Inside the newly created directory, run: ``pip install .``
* The setup script will install all required dependencies

Using geomdl-cli
================

``geomdl {command} {options}``

Available commands
------------------

* **help:** displays the command help
* **version:** displays the package version
* **plot:** plots single or multiple NURBS curves and surfaces using matplotlib
* **eval:** evaluates NURBS shapes and exports the evaluated points in various formats

Individual command help
-----------------------

``geomdl {command} --help``

Please run ``geomdl help`` for more details.

Documentation
=============

https://geomdl-cli.readthedocs.io/

Author
======

* Onur Rauf Bingol (`@orbingol <https://github.com/orbingol>`_)

License
=======

`MIT <LICENSE>`_


.. |RTD| image:: https://readthedocs.org/projects/geomdl-cli/badge/?version=latest
.. _|RTD| https://geomdl-cli.readthedocs.io/en/latest/?badge=latest
