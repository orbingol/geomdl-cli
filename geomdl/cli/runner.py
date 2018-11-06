"""

    geomdl-cli - Run NURBS-Python (geomdl) from the command line
    Copyright (c) 2018 Onur Rauf Bingol <orbingol@gmail.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""

#
# geomdl-cli command definitions
#

import sys
from geomdl import __version__ as base_version
from . import __version__ as cli_version
from . import __cli_usage__, __cli_commands__
from . import helpers_yaml
from . import helpers_nurbs


def command_help(**kwargs):
    """\
HELP: Displays geomdl-cli help\
    """
    # Display the package help
    print(__cli_usage__)
    # Display all available command help messages, including the user-defined commands
    print("Available commands:\n")
    for cmd in __cli_commands__.items():
        print("    " + cmd[0] + "\t\t" + cmd[1]['doc'])


def command_version(**kwargs):
    """\
VERSION: Displays geomdl-cli version\
    """
    print("geomdl-cli version", cli_version)
    print("geomdl version", base_version)


def command_plot(yaml_file_name, **kwargs):
    """\
PLOT: Plots NURBS curves and surfaces

"geomdl plot" command takes a YAML file as the input and plots the shapes defined in the file. \
The YAML file can contain single or multiple shapes. The YAML file format is described in the geomdl-cli documentation.

NURBS-Python library may be used to export curves and surfaces as YAML files. \
Please see "geomdl.exchange.export_yaml" documentation for details.

Usage:

    geomdl plot {yaml_file}                             plots the shape defined in the YAML file
    geomdl plot {yaml_file} --delta=0.1                 plots the shape using the evaluation delta of 0.1
    geomdl plot {yaml_file} --index=2                   plots the 2nd shape defined in the YAML file
    geomdl plot {yaml_file} --index=1 --delta=0.025     plots the 1st shape using the evaluation delta of 0.025

Available parameters:

    --help      displays this message
    --index=n   plots n-th curve or surface in the YAML file (works only for multi shapes)
    --delta=d   allows customization of the pre-defined evaluation delta in the YAML file. 0.0 < d < 1.0
    --name=fn   sets the file name for saving the figure (the figure window will not open if this parameter is set)

Notes:

    - If this command is too slow for you, please set the delta value to a bigger value, e.g. 0.05 or 0.1.
    - Please note that you may only export the figure in the file formats which matplotlib support.

Please see the documentation for more details.\
    """
    # Get keyword arguments
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    save_file_name = kwargs.get('name', None)

    # Process YAML file
    yaml_data = helpers_yaml.read_yaml_file(yaml_file_name)
    nurbs_data = yaml_data['shape']
    try:
        vis_data = yaml_data['visualization']
    except KeyError:
        vis_data = {}

    # Detect NURBS shape building function
    shape_types = dict(
        curve=dict(
            single=helpers_nurbs.build_curve_single,
            multi=helpers_nurbs.build_curve_multi,
        ),
        surface=dict(
            single=helpers_nurbs.build_surface_single,
            multi=helpers_nurbs.build_surface_multi,
        ),
    )

    try:
        build_func = shape_types[str(nurbs_data['type'])]
    except KeyError:
        print("Unsupported shape type: ", str(nurbs_data['type']), "\n")
        types_str = ", ".join([k for k in shape_types.keys()])
        print("Possible values are:", types_str)
        sys.exit(1)

    # Prepare render method parameters
    if save_file_name:
        render_params = dict(plot=False, filename=save_file_name)
    else:
        render_params = dict(plot=True)

    # Plot the NURBS object
    try:
        ns = helpers_nurbs.build_nurbs_shape(data=nurbs_data['data'], build_func=build_func,
                                             shape_delta=shape_delta, shape_idx=shape_idx)
        helpers_nurbs.build_vis(obj=ns, data=vis_data)
        ns.render(**render_params)
    except KeyError as e:
        print("Problem with the YAML file. The following key does not exist: {}".format(e.args[-1]))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)


def command_eval(yaml_file_name, **kwargs):
    """\
EVAL: Evaluates NURBS curves and surfaces

"geomdl eval" command takes a YAML file as the input and evaluated the shapes defined in the file. \
The YAML file can contain single or multiple shapes. The YAML file format is described in the geomdl-cli documentation.

The default behavior of the command is printing the evaluated surface or curve points to the screen. For multi curves \
and surfaces, there will be a "---" line between the evaluated points of the individual shapes. This command can also \
export the evaluated points in various formats, such as CSV, TXT and legacy VTK.

Usage:

    geomdl eval {yaml_file}                                 evaluates the shape and prints the points to the screen
    geomdl eval {yaml_file} --type=csv --name=test.csv      exports the evaluated points as a CSV file

Available parameters:

    --help      displays this message
    --index=n   plots n-th curve or surface in the YAML file (works only for multi shapes)
    --delta=d   allows customization of the pre-defined evaluation delta in the YAML file. 0.0 < d < 1.0
    --type=csv  defines the file type (csv, txt, vtk) for exporting the evaluated points
    --name=fn   sets the file name for exporting the evaluated points

Please see the documentation for more details.\
    """
    # Get keyword arguments
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    export_filename = kwargs.get('name', None)
    export_type = kwargs.get('type', 'screen')

    # Check user input
    possible_types = ['screen', 'csv', 'txt', 'vtk']
    if export_type not in possible_types:
        ptypes_str = ", ".join([pt for pt in possible_types])
        print("Cannot export in", str(export_type), "format. Possible types:", ptypes_str)
        sys.exit(1)

    if export_type != 'screen' and not export_filename:
        print("A file name is needed to export in", str(export_type), "format. Please use --name to set.")
        sys.exit(1)

    # Process YAML file
    yaml_data = helpers_yaml.read_yaml_file(yaml_file_name)
    nurbs_data = yaml_data['shape']

    # Detect NURBS shape building function
    shape_types = dict(
        curve=dict(
            single=helpers_nurbs.build_curve_single,
            multi=helpers_nurbs.build_curve_multi,
        ),
        surface=dict(
            single=helpers_nurbs.build_surface_single,
            multi=helpers_nurbs.build_surface_multi,
        ),
    )

    try:
        build_func = shape_types[str(nurbs_data['type'])]
    except KeyError:
        print("Unsupported shape type: ", str(nurbs_data['type']), "\n")
        types_str = ", ".join([k for k in shape_types.keys()])
        print("Possible values are:", types_str)
        sys.exit(1)

    # Plot the NURBS object
    try:
        ns = helpers_nurbs.build_nurbs_shape(data=nurbs_data['data'], build_func=build_func,
                                             shape_delta=shape_delta, shape_idx=shape_idx)
        helpers_nurbs.export_evalpts(obj=ns, file_name=export_filename, export_type=export_type)
    except KeyError as e:
        print("Problem with the YAML file. The following key does not exist: {}".format(e.args[-1]))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)
