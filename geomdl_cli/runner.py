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
from . import __usage__
from . import helpers_yaml
from . import helpers_nurbs


def command_help():
    print(__usage__)


def command_version():
    print("GEOMDL version ", __version__)


def command_plot(yaml_file):
    nurbs_data = helpers_yaml.read_yaml_file(yaml_file)
    try:
        vis_data = nurbs_data['visualization']
    except KeyError:
        vis_data = {}

    try:
        if nurbs_data['shape']['type'] == "curve":
            ns = helpers_nurbs.build_curve(nurbs_data['shape'])
            helpers_nurbs.build_vis(ns, vis_data)
            ns.render()
        elif nurbs_data['shape']['type'] == "surface":
            ns = helpers_nurbs.build_surface(nurbs_data['shape'])
            helpers_nurbs.build_vis(ns, vis_data)
            ns.render()
        else:
            print("Not a valid shape type. Possible types: curve, surface")
            sys.exit(1)
    except KeyError as e:
        print("Problem with the YAML file. The following key does not exist: {}".format(e.args[-1]))
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)
