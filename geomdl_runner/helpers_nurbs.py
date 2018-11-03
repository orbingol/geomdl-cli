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

from geomdl import NURBS


def build_curve(data):
    ns = NURBS.Curve()
    ns.degree = data['degree']
    try:
        ns.ctrlpts = data['control_points']['points']
        try:
            ns.weights = data['control_points']['weights']
        except KeyError:
            # geomdl will automatically set weights vector to 1
            pass
    except KeyError:
        ns.ctrlptsw = data['control_points']
    ns.knotvector = data['knot_vector']
    try:
        ns.delta = data['delta']
    except KeyError:
        # Use the default delta value
        pass
    return ns


def build_surface(data):
    pass
