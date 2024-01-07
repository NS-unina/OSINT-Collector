"""
Module containing all the globally accessible propertins and functions
"""

import os
import sys
from src.services.yaml_services import YAMLServices


class Globals:
    """
    Class containing all the globally accessible propertins and functions
    """

    @staticmethod
    def tools():
        """Return the available tool"""
        complete_path = os.path.join(os.getcwd(), 'tools')
        path_content = os.listdir(complete_path)

        folders = []
        for elem in path_content:
            if os.path.isdir(os.path.join(complete_path, elem)):
                folders.append(elem)

        return folders

    @staticmethod
    def help_message():
        """Return the help message"""

        tools = Globals.tools()

        return (
            "Usage:"
            "\n    launcher.py <tool> -i <input1> <input2> ..."
            "\n"
            "\nParameters:"
            f"\n    <tool>: Choose a tool from options: {tools}"
            "\n    -i <input>: Specify the input list."
            "\n"
            "\nExample:"
            "\n    python launcher.py the-harvester -i unina.it duckduckgo"
        )

    @staticmethod
    def help_tool_message():
        """
        Return the help message for a specific tool provided
        by command line input
        """

        tool = sys.argv[1]
        tool_config = YAMLServices.read_tool_config(tool)
        input_key = map(lambda item: item.key, tool_config.inputs)
        inputs_desc = map(lambda item: f"\n    {item.key}: {item.description}",
                          tool_config.inputs)

        inputs_keys_str = " ".join(input_key)
        inputs_desc = "".join(inputs_desc)

        return (
            "Usage:"
            f"\n    launcher.py {tool} -i {inputs_keys_str}"
            "\n"
            "\nDescription:"
            f"\n    {tool_config.description}"
            "\n"
            "\nInputs:"
            f"{inputs_desc}"
        )
