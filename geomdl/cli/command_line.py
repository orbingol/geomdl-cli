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
# Entry points for the Python packaging tools and command definitions
#

import sys
from . import runner

# Command definitions
CLI_DEFAULT_COMMANDS = dict(
    help=dict(
        doc="displays the help message",
        cmd=runner.command_help,
    ),
    version=dict(
        doc="displays the package version",
        cmd=runner.command_version,
    ),
    plot=dict(
        doc="plots single or multiple NURBS curves and surfaces using matplotlib",
        cmd=runner.command_plot,
        cmd_args=1,
    ),
    eval=dict(
        doc="evaluates NURBS shapes and exports the evaluated points in various formats",
        cmd=runner.command_eval,
        cmd_args=1,
    ),
)


def main():
    """Entry point for the "geomdl" command line script"""
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
        runner.command_help()
        sys.exit(0)

    # Command execution
    command = sys.argv[1]
    try:
        # Get command details
        current_command = CLI_DEFAULT_COMMANDS[command]

        # Print command help
        if "help" in command_params:
            print(current_command['cmd'].__doc__)
            sys.exit(0)

        # Execute command with command parameters
        try:
            cmd_args = current_command['cmd_args'] if 'cmd_args' in current_command else 0
            if cmd_args > 0:
                if argc - 2 < cmd_args:
                    # Print command help if there are no command arguments but expecting some
                    print(current_command['cmd'].__doc__)
                    sys.exit(0)
                # Call the command with the command arguments
                current_command['cmd'](*sys.argv[2:], **command_params)
            else:
                # Call the command without the command arguments
                current_command['cmd'](**command_params)
        except KeyError:
            print("Problem executing", str(command).upper(), "command. Please see the documentation for details.")
            sys.exit(1)
        except Exception as e:
            print("An error occurred: {}".format(e.args[-1]))
            sys.exit(1)
    except KeyError:
        print("The command", str(command).upper(), "does not exist. Please run 'geomdl help' for command reference.")
        sys.exit(1)
    except Exception as e:
        print("An error occurred: {}".format(e.args[-1]))
        sys.exit(1)

    # Command execution completed
    sys.exit(0)
