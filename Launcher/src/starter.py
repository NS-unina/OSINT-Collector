"""
The module is responsible of interactive with the inputs provided by
the user in order to validate them and makes them available for
the launcher
"""

import sys
import logging
from src.globals import Globals
from src.services.yaml_services import YAMLServices


class _Exceptions:
    """Manage starter errors"""

    invalid_format = ("Invalid format, please use 'launcher.py --help' "
                      "to understand how to use the tool")

    invalid_inputs = ("Wrong inputs, the following inputs "
                      "should be provided: %s")

    invalid_tool = ("Unknown tool, one the following tool "
                    "should be provided: %s")

    invalid_entrypoint = ("Unknown entrypoint, one the following entrypoint "
                          "should be provided: %s")


class Starter:
    """
    Class responsible of interactive with the inputs provided by
    the user in order to validate them and makes them available for
    the launcher
    """

    _log = logging.getLogger(__name__)
    _help_flag = ["--help", "-h"]

    @staticmethod
    def check_for_help():
        """
        Determines if the user requested an help
        """

        if len(sys.argv) == 2:
            help_input = sys.argv[1]
            if help_input in Starter._help_flag:
                return True

        return False

    @staticmethod
    def check_for_tool_help():
        """Returns True if the command is requesting help with a tool"""

        if len(sys.argv) == 3:
            help_input = sys.argv[2]
            tool_input = sys.argv[1]
            tools = Globals.tools()
            if help_input in Starter._help_flag and tool_input in tools:
                return True

        return False

    @staticmethod
    def fetch_launcher_params():
        """Determines which starter to use"""

        if len(sys.argv) == 1:
            # Interactive start
            tool, entry, inputs = Starter._interactive()
        else:
            # CMD start
            tool, entry, inputs = Starter._command_line_interface()

        Starter._check_tool_validity(tool)
        Starter._check_entry_validity(tool, entry)
        Starter._check_inputs_validity(tool, inputs)

        return tool, entry, inputs

    @staticmethod
    def _check_tool_validity(tool: str):
        """Check if tool is valid"""
        available_tools = Globals.tools()
        if tool not in available_tools:

            Starter._log.error(
                _Exceptions.invalid_tool,
                ", ".join(available_tools)
            )
            exit(1)

    @staticmethod
    def _check_entry_validity(tool: str, entry: str):
        """Check if the entrypoint has been provided"""
        tool_config = YAMLServices.read_tool_config(tool)
        tool_cfg_entry = tool_config.entrypoints

        filtered = filter(lambda item: item.key == entry, tool_cfg_entry)
        filtered_list = list(filtered)
        if len(filtered_list) == 0:

            tool_cfg_entry_keys = map(lambda item: item.key,
                                      tool_config.entrypoints)

            Starter._log.error(
                _Exceptions.invalid_entrypoint,
                ", ".join(tool_cfg_entry_keys)
            )
            exit(1)

    @staticmethod
    def _check_inputs_validity(tool: str, inputs: [str]):
        """Check if all inputs has been provided"""
        tool_config = YAMLServices.read_tool_config(tool)
        tool_cfg_in = tool_config.inputs
        if len(tool_cfg_in) != len(inputs):
            expected_inputs_keys = map(lambda item: item.key, tool_cfg_in)

            Starter._log.error(
                _Exceptions.invalid_inputs,
                ", ".join(expected_inputs_keys)
            )
            exit(1)

    @staticmethod
    def _command_line_interface():
        """Starter that get the image and inputs from the executed command"""

        # Check invalid format
        if len(sys.argv) < 6:
            Starter._log.error(_Exceptions.invalid_format)
            exit(1)

        tool_name = sys.argv[1]
        entry_flag = sys.argv[2]
        entry_value = sys.argv[3]
        input_flag = sys.argv[4]
        inputs_values = sys.argv[5:]

        # Check if the input flag is present
        if input_flag != "-i":
            Starter._log.error(_Exceptions.invalid_format)
            exit(1)

        if entry_flag != "-e":
            Starter._log.error(_Exceptions.invalid_format)
            exit(1)

        return tool_name, entry_value, inputs_values

    @staticmethod
    def _interactive():
        """Starter used to get tool and inputs interactively from user"""

        tool_list = Globals.tools()

        message = ""
        for index, elem in enumerate(tool_list):
            message += f"[{index}] {elem}\n"

        message += "Select tool (integer): "
        tool_index = int(input(message))

        tool = tool_list[tool_index]
        tool_config = YAMLServices.read_tool_config(tool)

        message = ""
        for index, elem in enumerate(tool_config.entrypoints):
            message += f"[{index}] {elem.key}\n"
        message += "Select entrypoint (integer): "
        entrypoint_index = int(input(message))
        entrypoint = tool_config.entrypoints[entrypoint_index]

        input_strings = []
        for item in tool_config.inputs:
            if item.key in entrypoint.inputs:
                input_strings.append(
                    input(f"Insert {item.key} ({item.description}): ")
                )

        return tool_list[tool_index], entrypoint, input_strings
