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
# File parsing and template processing functions for geomdl-cli
#

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

# Define custom Jinja2 template functions
CLI_TEMPLATE_FUNCTIONS = dict(
    knot_vector=geomdl.utilities.generate_knot_vector,
)


def process_jinja2_template(file_name):
    """Opens an input file, evaluates the Jinja2 template functions and returns the final file contents."""
    # Try to open the file
    try:
        with open(file_name, 'r') as fp:
            file_src = fp.read()
            file_src = file_src.replace("{%", "<%").replace("%}", "%>").replace("{{", "<{").replace("}}", "}>")
    except IOError:
        print("Cannot open file", str(file_name), "for reading. Check if the file exists.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)

    # Generate Jinja2 environment
    env = jinja2.Environment(
        loader=jinja2.DictLoader({file_name: file_src}),
        trim_blocks=True,
        block_start_string='<%', block_end_string='%>',
        variable_start_string='<{', variable_end_string='}>'
    )

    # Load custom functions into the Jinja2 environment
    for k, v in CLI_TEMPLATE_FUNCTIONS.items():
        env.globals[k] = v

    # Process Jinja2 template functions & variables inside the input file
    return env.get_template(file_name).render()


def read_yaml_file(yaml_file):
    """Opens a YAML file, parses it through Jinja2 and ruamel.yaml and returns a dict containing the YAML data"""
    yaml_src = process_jinja2_template(yaml_file)

    # Parse YAML after Jinja2 template processing
    yaml = YAML()
    data = yaml.load(yaml_src)

    # Return parsed YAML data
    return data
