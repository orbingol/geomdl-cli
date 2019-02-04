Using geomdl-cli
^^^^^^^^^^^^^^^^

geomdl-cli uses the following structure for executing the commands:

.. code-block:: console

    geomdl-cli {command} {options} {parameters}

where

* ``geomdl-cli`` is the name of the command line application
* ``{command}`` corresponds to the command to be executed, see the list below
* ``{options}`` corresponds to the command input
* ``{parameters}`` corresponds to the command parameters, such as ``--help`` or ``--delta``

Please see the individual command help for details on ``{options}`` and ``{parameters}`` values.

Available commands
==================

* ``help``: displays the help message
* ``version``: displays the package version
* ``config``: displays the configuration
* ``plot``: plots single or multiple NURBS curves and surfaces using `Matplotlib <https://matplotlib.org>`_
* ``eval``: evaluates NURBS shapes and exports the evaluated points in supported formats
* ``export``: exports NURBS shapes in supported CAD exchange formats

Individual command help
=======================

Individual command help can be displayed via ``--help`` parameter.

.. code-block:: console

    geomdl-cli {command} --help

where ``{command}`` corresponds to the command to be executed.

Defining input file format
==========================

By default, the input file format is determined from the file extension. However, in case of a file with no or different
extension, the input file format must be defined manually via ``--type`` parameter.

.. code-block:: console

    geomdl-cli {command} my_file --type=yaml

Supported input file formats: yaml, cfg, json

Examples
========

Please check the `GitHub repository <https://github.com/orbingol/geomdl-cli/tree/master/examples>`_ for example input
files.
