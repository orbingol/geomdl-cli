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
__version__ = "0.2.1"
__license__ = "MIT"

# Name of the command line script
__cli_name__ = "geomdl-cli"

# Command definitions
__cli_commands__ = dict(
    help=dict(
        doc="displays the help message",
        module="geomdl.cli.commands",
        func="command_help",
    ),
    version=dict(
        doc="displays the package version",
        module="geomdl.cli.commands",
        func="command_version",
    ),
    plot=dict(
        doc="plots single or multiple NURBS curves and surfaces using matplotlib",
        module="geomdl.cli.commands",
        func="command_plot",
        func_args=1,
    ),
    eval=dict(
        doc="evaluates NURBS shapes and exports the evaluated points in various formats",
        module="geomdl.cli.commands",
        func="command_eval",
        func_args=1,
    ),
)

# Custom configuration directory
__cli_dir__ = "." + __cli_name__

# Custom configuration file
__cli_file__ = __cli_name__ + ".json"

# Package help
__cli_usage__ = """\
GEOMDL-CLI - Run NURBS-Python (geomdl) from the command line

geomdl-cli is a command line tool for 'geomdl', a pure Python NURBS and B-Spline library.

Usage:

    geomdl {command} {options}

Individual command help available via

    geomdl {command} --help
"""
