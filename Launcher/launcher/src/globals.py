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
        """
        Return a list of available tools.

        This method retrieves the names of folders located within the 'tools'
        directory in the current working directory.

        Returns:
            list: A list containing the names of available tools (folders).
        """
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
            "\n    launcher.py <tool> -e <entrypoint> -i <input1> <input2> ..."
            "\n"
            "\nParameters:"
            f"\n    <tool>: Choose a tool from options: {tools}"
            "\n    -e <entrypoint>: Specify the entrypoint for the chosen tool"
            "\n    -i <input>: Specify the input list"
            "\n"
            "\nExample:"
            "\n    main.py the-harvester -e search-domain -i "
            "unina.it duckduckgo"
        )

    @staticmethod
    def help_tool_message():
        """
        Return the help message for a specific tool provided
        by command line input
        """

        tool = sys.argv[1]
        tool_config = YAMLServices.read_tool_config(tool)

        def space_separated_string(lst):
            return " ".join(lst)

        input_key = map(lambda item: item.key,
                        tool_config.inputs)
        inputs_desc = map(lambda item:
                          f"\n    {item.help_string()}",
                          tool_config.inputs)
        entrypoints_desc = map(lambda item: f"\n    {item.help_string()}",
                               tool_config.entrypoints)

        inputs_keys_str = space_separated_string(input_key)
        inputs_desc = "".join(inputs_desc)
        entrypoints = "".join(entrypoints_desc)

        return (
            "Usage:"
            f"\n    main.py {tool} -e <entrypoint> -i {inputs_keys_str}"
            "\n"
            "\nDescription:"
            f"\n    {tool_config.description}"
            "\n"
            "\nInputs:"
            f"{inputs_desc}"
            "\n"
            "\nEntrypoints:"
            f"{entrypoints}"
        )
