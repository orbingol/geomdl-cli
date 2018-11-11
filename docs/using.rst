Using geomdl-cli
^^^^^^^^^^^^^^^^

geomdl-cli uses the following structure for executing the commands:

.. code-block:: console

    geomdl-cli {command} {options} {parameters}

where

* ``geomdl-cli`` is the name of the command line application
* ``{command}`` corresponds to the command to be executed, such as **plot** or **eval**
* ``{options}`` corresponds to the command input
* ``{parameters}`` corresponds to the command parameters, such as **\--help** or **\--delta**

Please see the individual command help for details on ``{options}`` and ``{parameters}`` values.

Available commands
==================

The following command displays all default and user-defined commands along with a basic command usage information.

.. code-block:: console

    geomdl-cli help

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
