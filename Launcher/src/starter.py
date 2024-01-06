"""
The module is responsible of interactive with the inputs provided by
the user in order to validate them and makes them available for
the launcher
"""

import sys
import logging
from src.globals import tools
from src.services.yaml_services import read_tool_config


class StarterException(Exception):
    """Manage starter errors"""


class Starter:
    """
    Class responsible of interactive with the inputs provided by
    the user in order to validate them and makes them available for
    the launcher
    """

    _log = logging.getLogger(__name__)

    @staticmethod
    def check_for_help():
        """
        Determines if the user requested an help
        """
        help_flag = ["--help", "-h"]

        if len(sys.argv) == 2:
            help_input = sys.argv[1]
            if help_input in help_flag:
                return True

        return False

    @staticmethod
    def fetch_launcher_params():
        """Determines which starter to use"""

        if len(sys.argv) == 1:
            # Interactive start
            tool, inputs = Starter._interactive()
        else:
            # CMD start
            tool, inputs = Starter._command_line_interface()

        Starter._check_tool_validity(tool)
        Starter._check_inputs_validity(tool, inputs)

        return tool, inputs

    @staticmethod
    def _check_tool_validity(tool: str):
        """Check if tool is valid"""
        available_tools = tools()
        if tool not in available_tools:
            Starter._log.error(
                "Unknown tool, one the following tool should be provided: %s",
                ", ".join(available_tools)
            )
            raise StarterException("Invalid Tool")

    @staticmethod
    def _check_inputs_validity(tool: str, inputs: [str]):
        """Check if all inputs has been provided"""
        tool_config = read_tool_config(tool)
        tool_cfg_in = tool_config.inputs
        if len(tool_cfg_in) != len(inputs):
            expected_inputs_keys = map(lambda item: item.key, tool_cfg_in)

            Starter._log.error(
                "Wrong inputs, the following inputs should be provided: %s",
                ", ".join(expected_inputs_keys)
            )
            raise StarterException("Invalid Inputs")

    @staticmethod
    def _command_line_interface():
        """Starter that get the image and inputs from the executed command"""

        # Check invalid format
        if len(sys.argv) < 4:
            Starter._log.error("""
                Invalid format, please use 'launcher.py --help'
                to understand how to use the tool""")
            raise StarterException("Invalid format")

        tool_name = sys.argv[1]
        input_flag = sys.argv[2]
        inputs_values = sys.argv[3:]

        # Check if the input flag is present
        if input_flag != "-i":
            Starter._log.error("""
                Invalid format, please use 'launcher.py --help'
                to understand how to use the tool""")
            raise StarterException("Invalid input")

        return tool_name, inputs_values

    @staticmethod
    def _interactive():
        """Starter used to get tool and inputs interactively from user"""

        tool_list = tools()

        for index, elem in enumerate(tool_list):
            print(f"[{index}] {elem}")

        tool_index = int(input("Select tool (integer): "))

        tool = tool_list[tool_index]
        tool_config = read_tool_config(tool)

        input_strings = []
        for item in tool_config.inputs:
            input_strings.append(
                input(f"Insert {item.key} ({item.description}): ")
            )

        return tool_list[tool_index], input_strings
