#!/usr/bin/env python3

"""Main file"""

import logging
from src.globals import Globals
from src.launcher import Launcher
from src.starter import Starter

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    # Help Section

    if Starter.check_for_help():
        print(Globals.help_message())
        exit(0)

    if Starter.check_for_tool_help():
        print(Globals.help_tool_message())
        exit(0)

    # Launch Section

    image, inputs_str = Starter.fetch_launcher_params()
    launcher = Launcher(image, inputs_str)
    launcher.launch_tool()
