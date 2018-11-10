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

import os.path
from . import __version__
from . import __cli_usage__, __cli_commands__
from . import helpers_file
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
VERSION: Displays geomdl-cli and geomdl version\
    """
    print("geomdl-cli version", __version__)
    helpers_nurbs.print_version()


def command_plot(file_name, **kwargs):
    """\
PLOT: Plots NURBS curves and surfaces using Matplotlib

Usage:

    geomdl plot {file}                             plots the complete shape defined by the file
    geomdl plot {file} --delta=0.1                 plots the shape using the evaluation delta of 0.1
    geomdl plot {file} --index=2                   plots the 2nd shape defined in the input file
    geomdl plot {file} --index=1 --delta=0.025     plots the 1st shape using the evaluation delta of 0.025

Available parameters:

    --help          displays this message
    --type          defines the input file type
    --index=n       plots n-th curve or surface in the input file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the input fie. 0.0 < d < 1.0
    --name=fn       saves the figure as a file (the figure window will not open if this parameter is set)
    --vis           sets the visualization options

Notes:

    - If this command is too slow for you, please set the delta value to a bigger value, e.g. 0.05 or 0.1.
    - Please note that you may only export the figure in the file formats which matplotlib support.

Please see the documentation for more details.\
    """
    def parse_vis_options(options_str):
        row_sep = ";"
        col_sep = ":"
        off_on = {'off': False, 'on': True}
        options_arr = options_str.split(row_sep)
        ret_dict = {}
        print("Visualization options:")
        for idx, opt in enumerate(options_arr):
            opt = opt.strip().split(col_sep)
            if len(opt) != 2:
                continue
            opt[0] = opt[0].strip()
            opt[1] = opt[1].strip()
            if opt[1] in off_on:
                ret_dict[opt[0]] = off_on[opt[1]]
                print("- {k}: {v}".format(k=opt[0], v=opt[1]))
        return ret_dict

    # Get keyword arguments
    file_type = kwargs.get('type', '')
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    save_file_name = kwargs.get('name', None)
    vis_options = kwargs.get('vis', 'legend:off')

    # Prepare render method parameters
    if save_file_name:
        render_params = dict(plot=False, filename=save_file_name)
    else:
        render_params = dict(plot=True)

    # Open file and parse Jinja2 template
    temp_fn = helpers_file.read_input_file_with_template(file_name)

    try:
        # Plot the NURBS object
        ns = helpers_nurbs.generate_nurbs_from_file(
            file_name=temp_fn,
            delta=shape_delta,
            shape_idx=shape_idx,
            file_type=file_type
        )
        helpers_nurbs.build_vis(obj=ns, **parse_vis_options(vis_options))
        ns.render(**render_params)
    except KeyError as e:
        raise RuntimeError("Required key does not exist in the input data: {}".format(e.args[-1]))
    finally:
        # Close file
        helpers_file.close_input_file(temp_fn)


def command_eval(file_name, **kwargs):
    """\
EVAL: Evaluates NURBS curves and surfaces and prints the evaluated points or exports them as a file

The default behavior of the command is printing the evaluated surface or curve points to the screen. For multi curves \
and surfaces, there will be a "---" line between the evaluated points of the individual shapes. This command can also \
export the evaluated points in various formats, such as CSV, TXT and legacy VTK.

Usage:

    geomdl eval {file}                                 evaluates the shape and prints the points to the screen
    geomdl eval {file} --type=csv --name=test.csv      exports the evaluated points as a CSV file

Available parameters:

    --help          displays this message
    --type          defines the input file type
    --index=n       evaluates n-th curve or surface in the file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the file. 0.0 < d < 1.0
    --export=csv    defines the export file type (csv, txt, vtk)
    --name=fn       sets the export file name

Please see the documentation for more details.\
    """
    # Get keyword arguments
    file_type = kwargs.get('type', '')
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    export_filename = kwargs.get('name', None)
    export_type = kwargs.get('export', 'screen')

    # Check user input
    possible_types = ['screen', 'csv', 'txt', 'vtk']
    if export_type not in possible_types:
        ptypes_str = ", ".join([pt for pt in possible_types])
        raise RuntimeError("Cannot export in '" + str(export_type) + "'format. Possible types: " + ptypes_str)

    if export_type != 'screen' and not export_filename:
        error_str = "A file name is needed to export in '" + str(export_type) + "' format. Please use --name to set."
        raise RuntimeError(error_str)

    # Open file and parse Jinja2 template
    temp_fn = helpers_file.read_input_file_with_template(file_name)

    try:
        # Evaluate the NURBS object and display/export the evaluated points
        ns = helpers_nurbs.generate_nurbs_from_file(
            file_name=temp_fn,
            delta=shape_delta,
            shape_idx=shape_idx,
            file_type=file_type
        )
        helpers_nurbs.export_evalpts(obj=ns, file_name=export_filename, export_type=export_type)
    except KeyError as e:
        raise RuntimeError("Required key does not exist in the input data: {}".format(e.args[-1]))
    finally:
        # Close file
        helpers_file.close_input_file(temp_fn)


def command_export(file_name, **kwargs):
    """\
EXPORT: Exports NURBS curves and surfaces in supported formats

Please see 'geomdl.exchange' module documentation for details on export options.

Usage:

    geomdl export {file}                     exports the shape in pickle format (default)
    geomdl export {file} --type=cfg          exports the shape in libconfig format

Available parameters:

    --help          displays this message
    --index=n       exports n-th curve or surface in the input file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the input file. 0.0 < d < 1.0
    --export=csv    defines the export file type (default: json)
    --name=fn       sets the export file name (default: input path and name + new extension)

Please see the documentation for more details.\
    """
    def get_default_file_name(filename, extension):
        fname, fext = os.path.splitext(filename)
        fext = extension
        return fname + "." + fext

    # Get export type keyword argument
    export_type = kwargs.get('type', 'json')

    # Check user input
    possible_types = ['cfg', 'json', 'smesh', 'obj', 'stl', 'off']
    if export_type not in possible_types:
        ptypes_str = ", ".join([pt for pt in possible_types])
        raise RuntimeError("Cannot export in '" + str(export_type) + "' format. Possible types: " + ptypes_str)

    # Get remaining keyword arguments
    file_type = kwargs.get('type', '')
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    export_filename = kwargs.get('name', get_default_file_name(file_name, export_type))

    # Open file and parse Jinja2 template
    temp_fn = helpers_file.read_input_file_with_template(file_name)

    try:
        # Export the NURBS object
        ns = helpers_nurbs.generate_nurbs_from_file(
            file_name=temp_fn,
            delta=shape_delta,
            shape_idx=shape_idx,
            file_type=file_type
        )
        helpers_nurbs.export_nurbs(obj=ns, file_name=export_filename, export_type=export_type)
    except KeyError as e:
        raise RuntimeError("Required key does not exist in the input data: {}".format(e.args[-1]))
    finally:
        # Close file
        helpers_file.close_input_file(temp_fn)
