Configuration
^^^^^^^^^^^^^

geomdl-cli allows users to override existing commands and configuration variables with and option add custom commands
and configuration variables for the custom commands as well.

These changes can be directly applied by creating a special directory, ``.geomdl-cli``. geomdl-cli automatically
checks for the existence of this directory in the following locations:

* user home directory (e.g. ``/home/user/.geomdl-cli``, ``C:\Users\user\.geomdl-cli``)
* directory that you are running geomdl-cli

In the listed directories, geomdl-cli tries to load the custom configuration file ``config.json`` which is in JSON format
with special directives discussed below. If the file doesn't exist, geomdl-cli will continue working without any problems.

The following sections discuss the details of the JSON file and the customization options.

Structure of the config file
============================

The config file is structured as follows:

.. code-block:: json

    {
      "configuration": {
        "test_configuration": "default configuration data"
      },
      "commands": {
        "test": {
          "doc": "command documentation, displayed when 'geomdl-cli help' is called",
          "module": "geomdl-test.test",
          "func": "test_eval",
          "func_args": "0"
        }
      }
    }

There are two main sections: **configuration** and **commands**, which are used to create user-defined configuration
variables and commands for geomdl-cli.

In the example above, a command named ``test`` is created and this command will be executed when ``geomdl-cli test``
is called from the command line. A command definition can contain 4 elements:

* ``doc`` contains the text displayed when ``geomdl help`` is called
* ``func`` is the function to be called when the command is called, e.g. ``geomdl-cli test``
* ``func_args`` is the number of arguments that the function ``func`` takes
* ``module`` points to the Python module that is required to import for calling the function ``func``

Configuration variables will be available in the code via the following import statement:

.. code-block:: python

    from geomdl.cli import config

``config`` is a dictionary containing the default and the user-defined configuration variables. In the example above,
the configuration variable can be accessed using ``config['test_configuration']``.

Creating commands
=================

To be updated!

Overriding commands
===================

To be updated!

Creating configuration variables
================================

To be updated!

Overriding configuration variables
==================================

To be updated!
