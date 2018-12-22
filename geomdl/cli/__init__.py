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

__author__ = "Onur Rauf Bingol"
__version__ = "0.5.0"
__license__ = "MIT"

# Name of the command line script
__cli_name__ = "geomdl-cli"

# Command definitions
__cli_commands__ = dict(
    help=dict(
        desc="displays the help message",
        module="geomdl.cli.commands",
        func="command_help",
    ),
    version=dict(
        desc="displays the package version",
        module="geomdl.cli.commands",
        func="command_version",
    ),
    config=dict(
        desc="displays the configuration",
        module="geomdl.cli.commands",
        func="command_config",
    ),
    plot=dict(
        desc="plots single or multiple NURBS curves and surfaces using matplotlib",
        module="geomdl.cli.commands",
        func="command_plot",
        func_args=1,
    ),
    eval=dict(
        desc="evaluates NURBS shapes and exports the evaluated points in various formats",
        module="geomdl.cli.commands",
        func="command_eval",
        func_args=1,
    ),
    export=dict(
        desc="exports NURBS shapes in common CAD exchange formats",
        module="geomdl.cli.commands",
        func="command_export",
        func_args=1,
    ),
)

# Default configuration
__cli_config__ = dict(
    user_override=False,  # True if a user configuration is loaded, False otherwise
    plot_vis="legend:off",  # visualization options for plot command (--vis parameter)
    plot_name=None,  # figure save name option for plot command (--name parameter)
    eval_format="screen",  # export option for eval command (--format parameter)
    export_format="json",  # export file type option for export command (--format parameter)
)

# Custom configuration directory
__cli_config_dir__ = "." + __cli_name__

# Custom configuration file
__cli_config_file__ = "config.json"

# Variables for user convenience
config = __cli_config__
