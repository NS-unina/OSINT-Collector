#!/usr/bin/env python3

import sys
import subprocess
import os
from src.constants import *
from src.show_services import *
from src.kafka_services import *

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

    except subprocess.CalledProcessError as e:
        show_error("Error launching {}: {}".format(tool, e))

    # Manage output
    manage_output(tool)
    

def manage_output(tool: str):

    folder_path = './output/{}'.format(tool)
    if not os.path.exists(folder_path):
        show_error("Output folder does not exist")

    kafka = KafkaServices()
    
    # Iterate through each folder and subfolder to find
    # all the .json output file
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Check if file is a json
            if filename.lower().endswith('.json'):
                kafka.write(file_path=file_path)


def cmd_main():

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


def interactive_main():
    
    tools = read_compose_services()

    for index, elem in enumerate(tools):
        print("[{}] {}".format(index, elem))
    
    tool_index = int(input("Select tool (integer): "))
    input_string = input("Insert input (string): ")

    # Launch tool
    launch_tool(tools[tool_index], input_string)


if __name__ == "__main__":

    # Interactive launch
    if len(sys.argv) == 1:
        interactive_main()

    # Check hor help
    elif len(sys.argv) == 2:
        help_flag = ["--help", "-h"]
        help_input = sys.argv[1]
        if help_input in help_flag:
            show_usage()

    # Command line launch
    else:
        if len(sys.argv) != 4:
            show_error("Invalid format")

        cmd_main()
