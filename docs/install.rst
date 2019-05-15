Installing geomdl-cli
^^^^^^^^^^^^^^^^^^^^^

The recommended method for installation is using `pip <https://pypi.org/project/pip/>`_.

.. code-block:: console

    pip install --user geomdl.cli

Alternatively, you can install the latest development version from the GitHub repository:

* Clone the repository: ``git clone https://github.com/orbingol/geomdl-cli.git``
* Inside the directory containing the cloned repository, run: ``pip install --user .``
* The setup script will install all required dependencies

Docker Containers
=================

A collection of Docker containers is provided on `Docker Hub <https://hub.docker.com/r/idealabisu/nurbs-python/>`_
containing NURBS-Python, Cython-compiled core and the `command-line application <https://geomdl-cli.readthedocs.io>`_.
To get started, first install `Docker <https://www.docker.com/>`_ and then run the following on the Docker command
prompt to pull the image prepared with Python v3.5:

.. code-block:: console

    $ docker pull idealabisu/nurbs-python:py35

On the `Docker Repository <https://hub.docker.com/r/idealabisu/nurbs-python/>`_ page, you can find containers tagged for
Python versions and `Debian <https://www.debian.org/>`_ (no suffix) and `Alpine Linux <https://alpinelinux.org/>`_
(``-alpine`` suffix) operating systems.

After pulling your preferred image, run the following command:

.. code-block:: console

    $ docker run --rm -it --name geomdl -p 8000:8000 idealabisu/nurbs-python:py35

In all containers, Matplotlib is set to use ``webagg`` backend by default.
Please follow the instructions on the command line to view your figures.
