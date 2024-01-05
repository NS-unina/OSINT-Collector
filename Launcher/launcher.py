#!/usr/bin/env python3

import sys
import subprocess
import os
from src.globals import *
from src.services.kafka_services import *
from src.services.show_services import *
from src.services.yaml_services import *
from src.models.tool_config import *
from src.launchers.cmd_launcher import *
from src.launchers.interactive_launcher import *
from src.services.docker_services import *

def launch_tool(tool: str, inputs: [str]):

    tool_config = read_tool_config(tool)

    expected_inputs_keys = []
    for value in tool_config.inputs:
        expected_inputs_keys.append(value.key)

    if (tool not in tools()):
        show_error("Invalid tool")

    if (len(tool_config.inputs) != len(inputs)):
        expected_input_str = ", ".join(expected_inputs_keys)
        show_error("Wrong inputs, the following inputs should be provided: {}".format(expected_input_str))

    i = 0
    filled_entrypoint = tool_config.entrypoint
    for item in tool_config.inputs:
        filled_entrypoint = filled_entrypoint.replace("${}".format(item.key), inputs[i])
        i += 1

    working_dir = os.getcwd()
    image_tag = build_image(f'./tools/{tool}')
    run_container(
        image_tag=image_tag, 
        name=tool, 
        output_volume=f'{working_dir}/output/{tool}', 
        entrypoint=filled_entrypoint,
        timeout=False
    )

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


if __name__ == "__main__":

    args_len = len(sys.argv)

    # Help Section

    help_flag = ["--help", "-h"]

    if args_len == 2:
        help_input = sys.argv[1]
        if help_input in help_flag:
            show_usage()

    if args_len == 3:
        help_input = sys.argv[2]
        tool = sys.argv[1]
        if help_input in help_flag and tool in tools():
            show_tool_usage(tool)

    # Launch Section
    
    image = ""
    inputs_str = []

    if args_len == 1:
        # Interactive launch
        image, inputs_str = interactive_launcher()
    else:
        # CMD launch
        image, inputs_str = cmd_launcher()

    launch_tool(image, inputs_str)