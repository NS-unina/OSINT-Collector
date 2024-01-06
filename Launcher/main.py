#!/usr/bin/env python3

"""Main file"""

from src.services.show_services import show_usage
from src.launcher import Launcher, LauncherException
from src.starter import Starter, StarterException

if __name__ == "__main__":

    # Help Section

    if Starter.check_for_help():
        show_usage()

    # if args_len == 3:
    #     help_input = sys.argv[2]
    #     tool_input = sys.argv[1]
    #     if help_input in help_flag and tool_input in tools():
    #         show_tool_usage(tool_input)

    # Launch Section

    try:
        image, inputs_str = Starter.fetch_launcher_params()
        launcher = Launcher(image, inputs_str)
        launcher.launch_tool()

    except (StarterException, LauncherException):
        exit(1)
