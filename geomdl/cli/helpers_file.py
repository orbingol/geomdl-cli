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

import os
import shutil
import tempfile
import jinja2
from geomdl import utilities


# Define custom Jinja2 template functions
CLI_TEMPLATE_FUNCTIONS = dict(
    knot_vector=utilities.generate_knot_vector,
)


def process_jinja2_template(file_name):
    """Opens an input file, evaluates the Jinja2 template functions and returns the final file contents."""
    # Try to open the file
    try:
        with open(file_name, 'r') as fp:
            file_src = fp.read()
            file_src = file_src.replace("{%", "<%").replace("%}", "%>").replace("{{", "<{").replace("}}", "}>")
    except IOError:
        raise RuntimeError("Cannot open file '" + str(file_name) + "' for reading. Check if the file exists.")

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


def read_input_file_with_template(file_name):
    """Opens the input file, parses it with Jinja2 and returns the path and name of the final input file"""
    # Jinja2 template processing
    fsource = process_jinja2_template(file_name)
    fname = os.path.splitext(file_name)

    # Generate a temporary file and return its name
    return create_temp_file(fsource, fname[1])


def create_temp_file(file_contents, file_extension):
    """Creates a temporary file and returns its name"""
    # Generate the temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False) as fpt:
            fpt.write(file_contents.encode())
    except TypeError as e:
        print("Problem generating temporary file after template parsing")
        raise e

    # If the original file has an extension, concatenate it to the temporary file
    if file_extension:
        file_name = fpt.name + file_extension
        shutil.copy(fpt.name, file_name)
        os.unlink(fpt.name)
    else:
        file_name = fpt.name

    # Return the temporary file and its path
    return file_name


def close_input_file(file_name):
    """Deletes a file"""
    os.unlink(file_name)
