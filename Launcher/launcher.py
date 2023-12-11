#!/usr/bin/env python3

import sys
import subprocess
import os
from src.constants import *
from src.show_services import *

def launch_tool(tool: str, input: str):

    tools = read_compose_services()
    env = os.environ.copy()

    if (tool not in tools):
        show_error("Invalid tool")

    try:
        env["LAUNCHER_INPUT"] = input
        env["LAUNCHER_TOOL"] = tool
        result = subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'up', tool], check=True, env=env)
        
        if (result.returncode != 0):
            show_error("Error processing {}".format(tool))
        
        # Manage Output

    except subprocess.CalledProcessError as e:
        show_error("Error launching {}: {}".format(tool, e))

def main():

    image = sys.argv[1]
    input_flag = sys.argv[2]
    input_str = sys.argv[3]
    tools = read_compose_services()
    
    # Check if the tool is valid
    if (image not in tools):
        show_error("Invalid tool")

    # Check if the input flag is present
    if input_flag != "-i":
        show_error("Invalid input")
    
    # Launch tool
    launch_tool(image, input_str)


if __name__ == "__main__":

    # Check hor help
    if len(sys.argv) == 2:
        help_flag = ["--help", "-h"]
        help_input = sys.argv[1]
        if help_input in help_flag:
            show_usage()

    # Check if all args have been provided
    if len(sys.argv) != 4:
        show_error("Invalid format")

    main()
