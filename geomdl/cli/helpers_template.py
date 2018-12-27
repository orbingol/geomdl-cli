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
# Custom template functions for geomdl-cli
#

import math
from geomdl import utilities


def get_template_functions():
    """ Define custom Jinja2 template functions. """
    tmpl_funcs = dict(
        knot_vector=utilities.generate_knot_vector,
        sqrt=tmpl_sqrt,
        cubert=tmpl_cubert,
        pow=tmpl_pow
    )
    return tmpl_funcs


def tmpl_sqrt(x):
    """ Square-root of 'x'. """
    return math.sqrt(x)


def tmpl_cubert(x):
    """ Cube-root of 'x'. """
    return x ** (1.0 / 3.0) if x >= 0 else -(-x) ** (1.0 / 3.0)


def tmpl_pow(x, y):
    """ 'x' to the power 'y' """
    return math.pow(x, y)
