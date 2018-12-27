File Formats and Templating
^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

``knot_vector`` is a wrapper for `utilities.generate_knot_vector <https://nurbs-python.rtfd.io/en/latest/module_utilities.html#geomdl.utilities.generate_knot_vector>`_
function. ``{% set kv = knot_vector(3, 4) %}`` sets the output of the template function to the template variable **kv**.

The following is the list of custom template functions supported by geomdl-cli:

* ``knot_vector(d, np)``: generates a uniform knot vector. *d*: degree, *np*: number of control points
* ``sqrt(x)``:  square root of *x*
* ``cubert(x)``: cube root of *x*
* ``pow(x, y)``: *x* to the power of *y*
