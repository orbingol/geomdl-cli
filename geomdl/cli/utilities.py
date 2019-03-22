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
# NURBS evaluation and utility functions for geomdl-cli
#

import os
import os.path
from geomdl import __version__
from geomdl import NURBS
from geomdl import multi
from geomdl import exchange
from geomdl.visualization import VisMPL


# File types allowed for importing
CLI_FILE_IMPORT_TYPES = dict(
    cfg=exchange.import_cfg,
    conf=exchange.import_cfg,
    yaml=exchange.import_yaml,
    json=exchange.import_json,
)


def replace_extension(filename, extension):
    """Replaces file extension"""
    fname, fext = os.path.splitext(filename)
    fext = extension
    return fname + "." + fext


def print_version():
    """Prints geomdl version"""
    print("geomdl version", __version__)


def generate_nurbs_from_file(file_name, delta, shape_idx, file_type=''):
    """Generates NURBS objects from supported file formats"""
    # Fix input types
    delta = float(delta)
    shape_idx = int(shape_idx)

    # Try to find file type from its extension
    if not file_type:
        fname, fext = os.path.splitext(file_name)
        file_type = fext[1:]

    ftype = file_type.lower()
    if ftype in CLI_FILE_IMPORT_TYPES:
        # Build NURBS object
        nurbs_objs = CLI_FILE_IMPORT_TYPES[ftype](file_name, delta=delta, jinja2=True)

        # Return the shape
        if len(nurbs_objs) == 1:
            return nurbs_objs[0]

        if isinstance(nurbs_objs[0], NURBS.Curve):
            result = multi.CurveContainer(nurbs_objs)
        elif isinstance(nurbs_objs[0], NURBS.Surface):
            result = multi.SurfaceContainer(nurbs_objs)
        else:
            result = multi.VolumeContainer(nurbs_objs)

        # Set the delta for multi shape objects
        if 0.0 < delta < 1.0:
            result.delta = delta

        if shape_idx >= 0:
            return result[shape_idx]
        return result
    else:
        raise RuntimeError("The input file type '" + str(file_type) + "' is not supported")


def build_vis(obj, **kwargs):
    """ Prepares visualization module for the input spline geometry.

    :param obj: input spline geometry object
    :return: spline geometry object updated with a visualization module
    """
    vis_config = VisMPL.VisConfig(**kwargs)
    if isinstance(obj, (NURBS.Curve, multi.CurveContainer)):
        if obj.dimension == 2:
            obj.vis = VisMPL.VisCurve2D(vis_config)
        elif obj.dimension == 3:
            obj.vis = VisMPL.VisCurve3D(vis_config)
        else:
            raise RuntimeError("Can only plot 2- or 3-dimensional curves")

    if isinstance(obj, (NURBS.Surface, multi.SurfaceContainer)):
        obj.vis = VisMPL.VisSurface(vis_config)

    if isinstance(obj, (NURBS.Volume, multi.VolumeContainer)):
        obj.vis = VisMPL.VisVolume(vis_config)

    return obj


def export_evalpts(obj, file_name, export_format):
    """ Prints the evaluated points on the screen and optionally exports them to a file.

    :param obj: input curve or surface
    :type obj: NURBS.Curve, NURBS.Surface, Multi.CurveContainer or Multi.SurfaceContainer
    :param file_name: name of the export file
    :type file_name: str
    :param export_format: export file format, e.g. txt or csv
    :type export_format: str
    """
    if export_format == "csv":
        exchange.export_csv(obj, file_name, point_type='evalpts')
    elif export_format == "txt":
        exchange.export_txt(obj, file_name, point_type='evalpts')
    else:
        if isinstance(obj, multi.AbstractContainer):
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


def export_nurbs(obj, file_name, export_format):
    """ Exports NURBS data in common CAD exchange formats.

    :param obj: input spline geometry
    :param file_name: name of the export file
    :type file_name: str
    :param export_format: export file format, e.g. cfg, obj, stl, ...
    :type export_format: str
    """
    type_maps = dict(
        cfg=exchange.export_cfg,
        yaml=exchange.export_yaml,
        json=exchange.export_json,
        obj=exchange.export_obj,
        stl=exchange.export_stl,
        off=exchange.export_off,
        smesh=exchange.export_smesh,
        vmesh=exchange.export_vmesh,
    )

    try:
        type_maps[export_format](obj, file_name)
    except KeyError:
        raise RuntimeError("The export method '" + str(export_format) + "' has not been implemented yet")
