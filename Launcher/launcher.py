#!/usr/bin/env python3

import sys
import subprocess
import os
from src.constants import *
from src.services.kafka_services import *
from src.services.show_services import *
from src.services.yaml_services import *
from src.models.tool_config import *

tools = read_compose_services()

def launch_tool(tool: str, inputs: [str]):

    tool_config = read_tool_config(tool)

    expected_inputs_keys = []
    for value in tool_config.inputs:
        expected_inputs_keys.append(value.key)

    if (tool not in tools):
        show_error("Invalid tool")

    if (len(tool_config.inputs) != len(inputs)):
        expected_input_str = ", ".join(expected_inputs_keys)
        show_error("Missing inputs, the following inputs should be provided: {}".format(expected_input_str))

    try:

        # Setting env var
        env = os.environ.copy()
        
        i = 0
        filled_entrypoint = tool_config.entrypoint
        for item in tool_config.inputs:
            env[item.key] = inputs[i]
            filled_entrypoint = filled_entrypoint.replace("${}".format(item.key), inputs[i])
            i += 1

        env["LAUNCHER_ENTRYPOINT"] = filled_entrypoint
        env["LAUNCHER_TOOL"] = tool

        result = subprocess.run(['docker-compose', '-f', DOCKER_COMPOSE_PATH, 'up', 'common'], check=True, env=env)
        
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
    inputs_str = sys.argv[3:]
    
    # Check if the tool is valid
    if (image not in tools):
        show_error("Invalid tool")

    # Check if the input flag is present
    if input_flag != "-i":
        show_error("Invalid input")
    
    # Launch tool
    launch_tool(image, inputs_str)


def interactive_main():

    for index, elem in enumerate(tools):
        print("[{}] {}".format(index, elem))
    
    tool_index = int(input("Select tool (integer): "))

    tool = tools[tool_index]
    tool_config = read_tool_config(tool)

    input_strings = []
    for item in tool_config.inputs:    
        input_strings.append(input("Insert {} ({}): ".format(item.key, item.description)))

    # Launch tool
    launch_tool(tools[tool_index], input_strings)


if __name__ == "__main__":

    help_flag = ["--help", "-h"]

    # Interactive launch
    if len(sys.argv) == 1:
        interactive_main()

    # Check hor help
    elif len(sys.argv) == 2:
        help_input = sys.argv[1]
        if help_input in help_flag:
            show_usage()
    
    # Check hor tools help
    elif len(sys.argv) == 3:
        help_input = sys.argv[2]
        tool = sys.argv[1]
        if help_input in help_flag and tool in tools:
            show_tool_usage(tool)

    # Command line launch
    else:
        if len(sys.argv) < 4:
            show_error("Invalid format")

        cmd_main()
