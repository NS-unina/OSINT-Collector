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
        Starter._check_inputs_validity(tool, entry, inputs)

        return tool, entry, inputs

    @staticmethod
    def fetch_launcher_params_from_json(json: dict):
        """
        Determine the tool, entry point, and inputs based on the
        provided JSON data.

        This method extracts the tool name, entry point, and inputs from
        the provided JSON data, and then performs validity checks for
        the tool, entry point, and inputs.

        Args:
            json (dict): A dictionary containing the tool, entry point
            and inputs information.

        Returns:
            tuple: A tuple containing the tool name, entry point, and
            inputs if they are valid or None if not valid.
        """

        _tool = json.get("image")
        _entry = json.get("entrypoint")
        _inputs = json.get("inputs")

        if not Starter._check_tool_validity(_tool):
            return None, None, None

        if not Starter._check_entry_validity(_tool, _entry):
            return None, None, None

        if not Starter._check_inputs_validity(_tool, _entry, _inputs):
            return None, None, None

        return _tool, _entry, _inputs

    @staticmethod
    def _check_tool_validity(tool: str):
        """
        Check the validity of a tool.

        This method checks if the specified tool is valid by comparing it
        with the list of available tools.

        Args:
            tool (str): The name of the tool to be checked for validity.

        Returns:
            bool: A bool containing the check result.
        """
        available_tools = Globals.tools()
        if tool not in available_tools:

            Starter._log.error(
                _Exceptions.invalid_tool,
                ", ".join(available_tools)
            )

            return False

        return True

    @staticmethod
    def _check_entry_validity(tool: str, entry: str):
        """
        Check the validity of an entry point for the specified tool.

        This method checks if the provided entry point is valid for
        the specified tool by comparing it with the entry points
        defined in the tool's configuration.

        Args:
            tool (str): The name of the tool.
            entry (str): The entry point to be checked.

        Returns:
            bool: True if the entry point is valid, False otherwise.
        """
        tool_config = YAMLServices.read_tool_config(tool)

        if tool_config is None:
            return False

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

            return False

        return True

    @staticmethod
    def _check_inputs_validity(tool: str, entry: str, inputs: [str]):
        """
        Check the validity of provided inputs for the specified
        entry point of a tool.

        This method checks if all the required inputs for the specified
        entry point of the tool have been provided.

        Args:
            tool (str): The name of the tool.
            entry (str): The entry point of the tool.
            inputs (list of str): List of inputs provided for the entry point.

        Returns:
            bool: True if all inputs are valid, False otherwise.

        """

        tool_config = YAMLServices.read_tool_config(tool)
        if tool_config is None:
            return False

        tool_cfg_entry = tool_config.entrypoints
        filtered = filter(lambda item: item.key == entry, tool_cfg_entry)
        filtered_list = list(filtered)
        entrypoint = filtered_list[0]

        tool_cfg_in = entrypoint.inputs

        if len(tool_cfg_in) != len(inputs):
            expected_inputs_keys = map(lambda item: item, tool_cfg_in)

            Starter._log.error(
                _Exceptions.invalid_inputs,
                ", ".join(expected_inputs_keys)
            )
            return False

        return True

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
