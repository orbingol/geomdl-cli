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
# NURBS evaluation and utility functions
#

from geomdl import NURBS
from geomdl import Multi
from geomdl import exchange
from geomdl.visualization import VisMPL


def build_nurbs_shape(data, build_func, shape_idx, shape_delta):
    """Main function for generating NURBS objects from YAML files"""
    # Apply necessary conversions
    idx = int(shape_idx)
    delta = float(shape_delta)

    # Build NURBS shapes
    if isinstance(data, list):
        if len(data) == 1:
            ns = build_func['single'](data[0])
        elif idx >= 0:
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
    """Generates a NURBS curve"""
    ns = NURBS.Curve()
    ns.degree = data['degree']
    try:
        ns.ctrlpts = data['control_points']['points']
        if 'weights' in data['control_points']:
            ns.weights = data['control_points']['weights']
    except KeyError:
        ns.ctrlptsw = data['control_points']
    ns.knotvector = data['knotvector']
    if 'delta' in data:
        ns.delta = data['delta']
    return ns


def build_curve_multi(data):
    """Generates a NURBS multi-curve"""
    mns = Multi.MultiCurve()
    for d in data:
        ns = build_curve_single(d)
        mns.add(ns)
    return mns


def build_surface_single(data):
    """Generates a NURBS surface"""
    ns = NURBS.Surface()
    ns.degree_u = data['degree_u']
    ns.degree_v = data['degree_v']
    ns.ctrlpts_size_u = data['size_u']
    ns.ctrlpts_size_v = data['size_v']
    try:
        ns.ctrlpts = data['control_points']['points']
        if 'weights' in data['control_points']:
            ns.weights = data['control_points']['weights']
    except KeyError:
        ns.ctrlptsw = data['control_points']
    ns.knotvector_u = data['knotvector_u']
    ns.knotvector_v = data['knotvector_v']
    if 'delta' in data:
        ns.delta = data['delta']
    return ns


def build_surface_multi(data):
    """Generates a NURBS multi-surface"""
    mns = Multi.MultiSurface()
    for d in data:
        ns = build_surface_single(d)
        mns.add(ns)
    return mns


def build_vis(obj, data):
    """ Prepares visualization module for the input curve or surface.

    :param obj: input curve or surface
    :type obj: NURBS.Curve, NURBS.Surface, Multi.MultiCurve or Multi.MultiSurface
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


def export_evalpts(obj, file_name, export_type):
    """ Prints the evaluated points on the screen and optionally exports them to a file.

    :param obj: input curve or surface
    :type obj: NURBS.Curve, NURBS.Surface, Multi.MultiCurve or Multi.MultiSurface
    :param file_name: name of the export file
    :type file_name: str
    :param export_type: type of the export file, e.g. txt, csv or vtk
    :type export_type: str
    """
    if export_type == "csv":
        exchange.export_csv(obj, file_name, point_type='evalpts')
    elif export_type == "txt":
        exchange.export_txt(obj, file_name, point_type='evalpts')
    elif export_type == "vtk":
        exchange.export_txt(obj, file_name, point_type='evalpts')
    else:
        if isinstance(obj, Multi.Abstract.Multi):
            sz = len(obj)
            for idx, opt in enumerate(obj.evalpts):
                for pt in opt:
                    line = ", ".join([str(p) for p in pt])
                    print(line)
                if idx != sz - 1:
                    print("---")
        else:
            for pt in obj.evalpts:
                line = ", ".join([str(p) for p in pt])
                print(line)
