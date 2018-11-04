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

import sys

try:
    import geomdl
    import jinja2
    import ruamel.yaml
except ImportError:
    print("You should install geomdl, Jinja2 and ruamel.yaml packages before running this script.")
    sys.exit(1)

from ruamel.yaml import YAML
import geomdl.utilities


def _initialize_jinja2_funcs():
    custom_jinja2_funcs = dict(
        knot_vector=geomdl.utilities.generate_knot_vector,
    )
    return custom_jinja2_funcs


def _initialize_yaml_file(yaml_file):
    try:
        with open(yaml_file, 'r') as fp:
            yaml_str = fp.read()
            yaml_str = yaml_str.replace("{%", "<%").replace("%}", "%>").replace("{{", "<{").replace("}}", "}>")
    except IOError:
        print("Cannot open file", str(yaml_file), "for reading. Check if the file exists.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)

    return yaml_str


def read_yaml_file(yaml_file):
    yaml_source = _initialize_yaml_file(yaml_file)
    env = jinja2.Environment(
        loader=jinja2.DictLoader({yaml_file: yaml_source}),
        trim_blocks=True,
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<{', variable_end_string='}>'
    )
    custom_funcs = _initialize_jinja2_funcs()
    for k, v in custom_funcs.items():
        env.globals[k] = v
    yaml_str = env.get_template(yaml_file).render()

    # Parse YAML string after Jinja2 processing
    yaml = YAML()
    data = yaml.load(yaml_str)

    return data


