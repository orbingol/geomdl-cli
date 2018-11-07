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
# Entry point definitions for Python packaging tools
#

import os
import os.path
import sys
import importlib
import json
from . import __cli_name__, __cli_commands__, __cli_dir__, __cli_file__


def read_custom_config(root_dir):
    """ Reads custom configuration files and adds them to the command list.

    :param root_dir: root directory containing the custom configuration
    """
    config_dir = os.path.join(root_dir, __cli_dir__)
    config_file = os.path.join(config_dir, __cli_file__)
    if os.path.isfile(config_file):
        # Add config directory to the path
        sys.path.append(config_dir)
        # Open config file
        try:
            with open(config_file, 'r') as fp:
                # Load the JSON file
                json_str = json.load(fp)
                # Add custom commands to the commands dictionary
                __cli_commands__.update(json_str)
        except IOError:
            print("Cannot read", config_file, "for reading. Skipping...")
        except Exception as e:
            print("Error while reading custom configuration file {fn}: {e}".format(fn=config_file, e=e.args[-1]))
            sys.exit(1)


def main():
    """Entry point for the command line application"""
    # Default user configuration directories
    user_config_root_dirs = [os.getcwd(), os.path.expanduser("~")]
    # Load user commands
    for root_dir in user_config_root_dirs:
        read_custom_config(root_dir)

    # Extract command parameters and update sys.argv
    command_params = {}
    new_sysargv = []
    for s in sys.argv:
        if s.startswith("--"):
            s_arr = s[2:].split("=")
            try:
                command_params[s_arr[0]] = s_arr[1]
            except IndexError:
                command_params[s_arr[0]] = 1
        else:
            new_sysargv.append(s)
    sys.argv = new_sysargv

    # Get number of command line arguments
    argc = len(sys.argv)

    # Show help if there are no command line arguments
    if argc < 2:
        print("No commands specified. Please run '" + __cli_name__ + " help' to see the list of commands available.")
        sys.exit(0)

    # Command execution
    try:
        # Load the command information from the command dictionary
        command = __cli_commands__[sys.argv[1]]

        # Import the module and get the function to be executed
        module = importlib.import_module(command['module'])
        func = getattr(module, command['func'])

        # Print command help if "--help" is present in the command arguments
        if "help" in command_params:
            print(func.__doc__)
            sys.exit(0)

        # Run the command
        try:
            cmd_args = command['func_args'] if 'func_args' in command else 0
            if cmd_args > 0:
                if argc - 2 < cmd_args:
                    # Print command help if there are no command arguments but expecting some
                    print(func.__doc__)
                    sys.exit(0)
                # Call the command with the command arguments
                func(*sys.argv[2:], **command_params)
            else:
                # Call the command without the command arguments
                func(**command_params)
        except KeyError:
            print("Problem executing", str(sys.argv[1]).upper(), "command. Please see the documentation for details.")
            sys.exit(1)
        except Exception as e:
            print("An error occurred: {}".format(e.args[-1]))
            sys.exit(1)
    except KeyError:
        print("The command", str(sys.argv[1]).upper(), "is not available. Please run '" + __cli_name__ +
              " help' to see the list of commands available.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)

    # Command execution completed
    sys.exit(0)
