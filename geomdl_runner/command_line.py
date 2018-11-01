"""

    geomdl_runner - Run NURBS-Python (geomdl) from the command line
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

import sys
from . import __version__
from . import runner


__usage__ = """\
GEOMDL - A pure Python NURBS library

Usage:

    geomdl {command} {options}

1) Plotting curves or surfaces:

    geomdl plot curve.yaml

"""


def main():
    argc = len(sys.argv)
    if argc < 2:
        print(__usage__)
        sys.exit(0)

    command = sys.argv[1]

    # Command: help
    if command == "help":
        print(__usage__)
        sys.exit(0)

    # Command: version
    if command == "version":
        print("GEOMDL version ", __version__)
        sys.exit(0)

    # Command: plot
    if command == "plot":
        if argc < 3:
            print("ERROR: plot command requires at least 1 argument")
        runner.plot_nurbs(sys.argv[2])
        sys.exit(0)
