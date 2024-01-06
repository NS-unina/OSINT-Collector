#!/usr/bin/env python3

"""
Entrypoint of the launcher
"""

import sys
import os
from src.globals import tools
from src.services.kafka_services import KafkaServices
from src.services.show_services import show_error, show_tool_usage, show_usage
from src.services.yaml_services import read_tool_config
from src.launchers.cmd_launcher import cmd_launcher
from src.launchers.interactive_launcher import interactive_launcher
from src.services.docker_services import build_image, run_container


def launch_tool(tool: str, inputs: [str]):
    """
    Function used to start the docker container with the choosed tool
    """

    tool_config = read_tool_config(tool)

    expected_inputs_keys = []
    for value in tool_config.inputs:
        expected_inputs_keys.append(value.key)

    if tool not in tools():
        show_error("Invalid tool")

    if len(tool_config.inputs) != len(inputs):
        incipit = "Wrong inputs, the following inputs should be provided"
        expected_input_str = ", ".join(expected_inputs_keys)
        show_error(f"{incipit}: {expected_input_str}")

    i = 0
    filled_entrypoint = tool_config.entrypoint
    for item in tool_config.inputs:
        cursor = f"${item.key}"
        value = inputs[i]

        filled_entrypoint = filled_entrypoint.replace(cursor, value)
        i += 1

    working_dir = os.getcwd()
    image_tag = build_image(f'./tools/{tool}')
    run_container(image_tag=image_tag,
                  name=tool,
                  output_volume=f'{working_dir}/output/{tool}',
                  entrypoint=filled_entrypoint)

    # Manage output
    manage_output(tool)


def manage_output(tool: str):
    """
    Function used to get the tool output and send it to kafka
    """

    folder_path = f'./output/{tool}'
    if not os.path.exists(folder_path):
        show_error("Output folder does not exist")

    kafka = KafkaServices()

    # Iterate through each folder and subfolder to find
    # all the .json output file
    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if file is a json
            if filename.lower().endswith('.json'):
                kafka.write(file_path=file_path)


if __name__ == "__main__":

    args_len = len(sys.argv)

    # Help Section

    help_flag = ["--help", "-h"]

    if args_len == 2:
        help_input = sys.argv[1]
        if help_input in help_flag:
            show_usage()

    if args_len == 3:
        help_input = sys.argv[2]
        tool_input = sys.argv[1]
        if help_input in help_flag and tool_input in tools():
            show_tool_usage(tool_input)

    # Launch Section

    if args_len == 1:
        # Interactive launch
        image, inputs_str = interactive_launcher()
    else:
        # CMD launch
        image, inputs_str = cmd_launcher()

    launch_tool(image, inputs_str)
