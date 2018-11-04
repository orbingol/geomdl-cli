"""

    geomdl_cli - Run NURBS-Python (geomdl) from the command line
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
from geomdl import Multi
from geomdl.visualization import VisMPL


def build_nurbs_shape(data, build_func, shape_idx, shape_delta):
    # Apply necessary conversions
    idx = int(shape_idx)
    delta = float(shape_delta)

    # Build NURBS shapes
    if len(data) > 1:
        if idx >= 0:
            ns = build_func['single'](data[idx])
        else:
            ns = build_func['multi'](data)
    else:
        ns = build_func['single'](data)

    # Set delta value
    if delta > 0:
        ns.delta = delta
    return ns


def build_curve_single(data):
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
    ns.knotvector = data['knotvector']
    try:
        ns.delta = data['delta']
    except KeyError:
        # Use the default delta value
        pass
    return ns


def build_curve_multi(data):
    mns = Multi.MultiCurve()
    for d in data:
        ns = build_curve_single(d)
        mns.add(ns)
    return mns


def build_surface_single(data):
    ns = NURBS.Surface()
    ns.degree_u = data['degree_u']
    ns.degree_v = data['degree_v']
    ns.ctrlpts_size_u = data['size_u']
    ns.ctrlpts_size_v = data['size_v']
    try:
        ns.ctrlpts = data['control_points']['points']
        try:
            ns.weights = data['control_points']['weights']
        except KeyError:
            # geomdl will automatically set weights vector to 1
            pass
    except KeyError:
        ns.ctrlptsw = data['control_points']
    ns.knotvector_u = data['knotvector_u']
    ns.knotvector_v = data['knotvector_v']
    try:
        ns.delta = data['delta']
    except KeyError:
        # Use the default delta value
        pass
    return ns


def build_surface_multi(data):
    mns = Multi.MultiSurface()
    for d in data:
        ns = build_surface_single(d)
        mns.add(ns)
    return mns


def build_vis(obj, data):
    """ Prepares visualization module for the input curve or surface.

    :param obj: input curve or surface
    :type obj: NURBS.Curve or NURBS.Surface
    :param data: visualization options
    :type data: dict
    :return: curve or surface updated with a visualization module
    """
    vis_config = VisMPL.VisConfig(**data)
    if isinstance(obj, (NURBS.Curve, Multi.MultiCurve)):
        if obj.dimension == 2:
            obj.vis = VisMPL.VisCurve2D(vis_config)
        elif obj.dimension == 3:
            obj.vis = VisMPL.VisCurve3D(vis_config)
        else:
            raise ValueError("Can only plot 2- or 3-dimensional curves")

    if isinstance(obj, (NURBS.Surface, Multi.MultiSurface)):
        obj.vis = VisMPL.VisSurfTriangle(vis_config)

    return obj
