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
__version__ = "0.1.2"
__license__ = "MIT"

__usage__ = """\
GEOMDL-CLI - Run geomdl from the command line

geomdl-cli is a command line tool for geomdl (NURBS-Python), a pure Python NURBS and B-Spline library.

Usage:

    geomdl {command} {options}

Individual command help available via

    geomdl {command} --help

Available commands:

    help        displays this message
    version     displays the package version
    plot        plots single or multiple NURBS curves and surfaces using matplotlib
    eval        evaluates NURBS shapes and exports the evaluated points in various formats\
"""
