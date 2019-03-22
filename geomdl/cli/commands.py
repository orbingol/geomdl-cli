"""

    geomdl-cli - Run NURBS-Python (geomdl) from the command line
    Copyright (c) 2018-2019 Onur Rauf Bingol <orbingol@gmail.com>

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
from . import __version__
from . import __cli_commands__
from . import config
from . import utilities


def command_help(**kwargs):
    """\
HELP: Displays geomdl-cli help\
    """
    help_text = """\
GEOMDL-CLI - Run NURBS-Python (geomdl) from the command line

geomdl-cli is a command line tool for 'geomdl', a pure Python NURBS and B-Spline library.

Usage:

    geomdl-cli {command} {options}

Individual command help available via

    geomdl-cli {command} --help
"""
    # Display the package help
    print(help_text)
    # Display all available command help messages, including the user-defined commands
    print("Available commands:\n")
    for cmd in __cli_commands__.items():
        print("    " + cmd[0] + "\t\t" + cmd[1]['desc'])


def command_version(**kwargs):
    """\
VERSION: Displays geomdl-cli and geomdl version\
    """
    print("geomdl-cli version", __version__)
    utilities.print_version()


def command_config(**kwargs):
    """\
CONFIG: Displays geomdl-cli configuration\
    """
    print("Configuration variables:")
    for cfg in config.items():
        print("- {k}: {v}".format(k=cfg[0], v=cfg[1]))


def command_plot(file_name, **kwargs):
    """\
PLOT: Plots NURBS curves and surfaces using matplotlib

'geomdl-cli plot' command takes a supported file type as an input and plots the NURBS curves and/or surfaces in the \
input file. The supported file types are: libconfig (.cfg), YAML (.yaml) and JSON (.json)

The input files can be created manually or can be exported via appropriate 'geomdl' API call. Please see \
'geomdl.exchange' documentation for importing and exporting NURBS shapes in the supported file formats.

Usage:

    geomdl-cli plot {file}                             plots the complete shape defined by the input file
    geomdl-cli plot {file} --delta=0.1                 plots the shape using the evaluation delta of 0.1
    geomdl-cli plot {file} --index=2                   plots the 2nd shape defined in the input file
    geomdl-cli plot {file} --index=1 --delta=0.025     plots the 1st shape using the evaluation delta of 0.025

Available parameters:

    --help          displays this message
    --type=t        defines the input file type
    --index=n       plots n-th curve or surface in the input file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the input file (0.0 < d < 1.0)
    --name=fn       saves the figure as a file (the figure window will not open if this parameter is set)
    --vis           sets the visualization options

Configuration variables:

    plot_vis        default value for '--vis' parameter
    plot_name       default value for '--name' parameter

Visualization options:

'--vis' parameter can be used for changing visualization options. The visualization options are documented on:

https://nurbs-python.readthedocs.io/en/latest/module_vis_mpl.html#geomdl.visualization.VisMPL.VisConfig

The following examples illustrate some ways to input the visualization options to 'geomdl-cli':

    - geomdl-cli plot {file} --vis="ctrlpts:off;axes:off"       no control points and axes are displayed
    - geomdl-cli plot {file} --vis="legend:on"                  figure legend is displayed
    - geomdl-cli plot {file} --vis="evalpts:off;legend:on"      surface or curve is not displayed, legend is displayed

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
    save_file_name = kwargs.get('name', config['plot_name'])
    vis_options = kwargs.get('vis', config['plot_vis'])

    # Prepare render method parameters
    if save_file_name:
        render_params = dict(plot=False, filename=save_file_name)
    else:
        render_params = dict(plot=True)

    # Plot the NURBS object
    ns = utilities.generate_nurbs_from_file(
        file_name=file_name,
        delta=shape_delta,
        shape_idx=shape_idx,
        file_type=file_type
    )
    utilities.build_vis(obj=ns, **parse_vis_options(vis_options))
    ns.render(**render_params)


def command_eval(file_name, **kwargs):
    """\
EVAL: Evaluates NURBS curves and surfaces and prints the evaluated points or exports them as a file

'geomdl-cli eval' command takes a supported file type as an input and plots the NURBS curves and/or surfaces in the \
input file. The supported file types are: libconfig (.cfg), YAML (.yaml) and JSON (.json)

The input files can be created manually or can be exported via appropriate 'geomdl' API call. Please see \
'geomdl.exchange' documentation for importing and exporting NURBS shapes in the supported file formats.

The default behavior of the command is printing the evaluated surface or curve points to the screen. For multi curves \
and surfaces, there will be a "---" line between the evaluated points of the individual shapes. This command can also \
export the evaluated points in various formats, such as CSV, TXT and legacy VTK.

Usage:

    geomdl-cli eval {file}                                 evaluates the shape and prints the points to the screen
    geomdl-cli eval {file} --format=csv --name=test.csv    exports the evaluated points in CSV format as 'test.csv'

Available parameters:

    --help          displays this message
    --type=t        defines the input file type
    --index=n       evaluates n-th curve or surface in the file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the file (0.0 < d < 1.0)
    --format=f      defines the export file format (f should be one of them: screen, csv, txt or vtk)
    --name=fn       sets the export file name (default fn = input path and name + new extension)

Configuration variables:

    eval_format     default value for '--format' parameter

Please see the documentation for more details.\
    """
    # Get keyword arguments
    export_format = kwargs.get('format', config['eval_format'])

    # Check user input
    possible_types = ['screen', 'csv', 'txt', 'vtk']
    if export_format not in possible_types:
        ptypes_str = ", ".join([pt for pt in possible_types])
        raise RuntimeError("Cannot export in '" + str(export_format) + "' format. Possible types: " + ptypes_str)

    file_type = kwargs.get('type', '')
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    export_filename = kwargs.get('name', utilities.replace_extension(file_name, export_format))

    # Evaluate the NURBS object and display/export the evaluated points
    ns = utilities.generate_nurbs_from_file(
        file_name=file_name,
        delta=shape_delta,
        shape_idx=shape_idx,
        file_type=file_type
    )
    utilities.export_evalpts(obj=ns, file_name=export_filename, export_format=export_format)


def command_export(file_name, **kwargs):
    """\
EXPORT: Exports NURBS curves and surfaces in supported formats

'geomdl-cli export' command takes a supported file type as an input and plots the NURBS curves and/or surfaces in the \
input file. The supported file types are: libconfig (.cfg), YAML (.yaml) and JSON (.json)

The input files can be created manually or can be exported via appropriate 'geomdl' API call. Please see \
'geomdl.exchange' documentation for importing and exporting NURBS shapes in the supported file formats.

The following file types are supported for exporting: cfg, yaml, json, smesh, obj, stl, off. \
Please see 'geomdl.exchange' module documentation for details on file export options.

Usage:

    geomdl-cli export {file}                     exports the shape in pickle format (default)
    geomdl-cli export {file} --format=cfg        exports the shape in libconfig format

Available parameters:

    --help          displays this message
    --type=t        defines the input file type
    --index=n       exports n-th curve or surface in the input file (works only for multi shapes)
    --delta=d       overrides pre-defined evaluation delta in the input file (0.0 < d < 1.0)
    --format=f      defines the export file type (default f = json)
    --name=fn       sets the export file name (default fn = input path and name + new extension)

Configuration variables:

    export_format   default value for '--format' parameter

Please see the documentation for more details.\
    """
    # Get export type keyword argument
    export_format = kwargs.get('format', config['export_format'])

    # Check user input
    possible_types = ['cfg', 'yaml', 'json', 'obj', 'stl', 'off', 'smesh', 'vmesh']
    if export_format not in possible_types:
        ptypes_str = ", ".join([pt for pt in possible_types])
        raise RuntimeError("Cannot export in '" + str(export_format) + "' format. Possible types: " + ptypes_str)

    # Get remaining keyword arguments
    file_type = kwargs.get('type', '')
    shape_idx = kwargs.get('index', -1)
    shape_delta = kwargs.get('delta', -1.0)
    export_filename = kwargs.get('name', utilities.replace_extension(file_name, export_format))

    # Export the NURBS object
    ns = utilities.generate_nurbs_from_file(
        file_name=file_name,
        delta=shape_delta,
        shape_idx=shape_idx,
        file_type=file_type
    )
    utilities.export_nurbs(obj=ns, file_name=export_filename, export_format=export_format)


