#!/usr/bin/env python3

import sys
import subprocess
import os

tools = {
    1: 'instaloader'
}

def show_usage():
    print("Usage:")
    print("    launcher.py <tool> -i <input>")
    print("\nParameters:")
    print("    <tool>: Choose a tool from options:", ", ".join(tools.values()))
    print("    -i <input>: Specify the input as a string.")
    print("\nExample:")
    print("    python launcher.py instaloader -i uninait")
    sys.exit(0)

def show_error(error: str):
    print("[LauncherError] {}".format(error))
    sys.exit(1)

def launch_tool(tool: str, input: str):
    try:
        env = os.environ.copy()
        env["LAUNCHER_INPUT"] = input
        result = subprocess.run(['docker-compose', '-f', './{}/docker-compose.yml'.format(tool), 'up',], check=True, env=env)
        
        if (result.returncode != 0):
            show_error("Error processing {}".format(tool))
        
        # Manage Output

    except subprocess.CalledProcessError as e:
        show_error("Error launching {}: {}".format(tool, e))

def main():

    image = sys.argv[1]
    input_flag = sys.argv[2]
    input_str = sys.argv[3]
    
    # Check if the tool is valid
    if (image not in tools.values()):
        show_error("Invalid tool")

    # Check if the input flag is present
    if input_flag != "-i":
        show_error("Invalid input")
    
    # Launch tool
    if (image in tools.values()):
        launch_tool(image, input_str)
    else:
        show_error("Invalid tool")


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
