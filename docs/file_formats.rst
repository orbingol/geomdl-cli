Supported File Formats and Templating
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Unless defined otherwise in the command help (``geomdl-cli {command} --help``), any command in need of a NURBS data
input usse the following file formats: libconfig, YAML and JSON.
Please see `geomdl documentation <https://nurbs-python.readthedocs.io/en/latest/file_formats.html>`_ for details on the
supported file formats.

Using Jinja2 templates in input files
=====================================

The following YAML file describes a 3-dimensional Bézier curve:

.. code-block:: yaml

    {% set degree = 3 %}
    {% set kv = knot_vector(3, 4) %}

    shape:
      type: curve
      data:
        degree: {{ degree }}
        knotvector: {{ kv }}
        control_points:
          points:
            - [10, 5, 10]
            - [10, 20, -30]
            - [40, 10, 25]
            - [-10, 5, 0]

The tags ``{%`` and ``%}`` define Jinja2 template statements, ``{{`` and ``}}`` define expressions to print to the
template output. ``{% set degree = 3 %}`` simply creates a template variable **degree** which can be used to replace
integer ``3``. This variable is used to set the curve degree with ``{{ degree }}``.

geomdl-cli also defines a template function **knot_vector(d, np)** where *d* is the degree and *np* is the number of
control points. It is a wrapper function for geomdl's *utilities.generate_knot_vector* function and they both take the
same number of input parameters. ``{% set kv = knot_vector(3, 4) %}`` sets the output of the template function to the
template variable **kv**.

Available template functions in geomdl-cli package and what they are wrapping are listed below:

* ``knot_vector``: geomdl.utilities.generate_knot_vector
