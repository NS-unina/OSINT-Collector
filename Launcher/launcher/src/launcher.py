"""
The module is responsible for handling the startup of the tool and
manage it's output and lifecycle
"""

import logging
from src.globals import Globals
from src.services.yaml_services import YAMLServices
from src.services.docker_services import DockerServices


class _Exceptions:
    """Manage launcher errors"""

    invalid_inputs = ("Wrong inputs, the following inputs "
                      "should be provided: %s")

    invalid_tool = ("Unknown tool, one the following tool "
                    "should be provided: %s")

    invalid_entrypoint = ("Unknown entrypoint, one the following entrypoint "
                          "should be provided: %s")

    invalid_output_folder = "Output folder %s does not exist"


class Launcher:
    """
    Class responsible for handling the startup of the tool and
    manage it's output and lifecycle
    """

    _log = logging.getLogger(__name__)

    def __init__(self, tool: str, entrypoint: str, inputs: [str]):
        """
        Initialize the launcher with the provided value

        Raises: LauncherException
        If there is an error during the initialization.
        """
        self.tool = tool
        self.entrypoint = entrypoint
        self.inputs = inputs
        self.tool_config = YAMLServices.read_tool_config(self.tool)

        # Check if tool is valid
        available_tools = Globals.tools()
        if self.tool not in available_tools:
            self._log.error(
                _Exceptions.invalid_tool,
                ", ".join(available_tools)
            )
            exit(1)

        # Check if entrypoint is valid
        matching_entrypoints = list(filter(lambda item: item.key == entrypoint,
                                           self.tool_config.entrypoints))
        if not any(matching_entrypoints):

            tool_cfg_entry_keys = map(lambda item: item.key,
                                      self.tool_config.entrypoints)

            self._log.error(
                _Exceptions.invalid_entrypoint,
                ", ".join(tool_cfg_entry_keys)
            )
            exit(1)

        # Check if all inputs has been provided
        entrypoint_config = matching_entrypoints[0]
        tool_cfg_in = entrypoint_config.inputs
        if len(tool_cfg_in) != len(inputs):
            expected_inputs_keys = map(lambda item: item.key, tool_cfg_in)

            self._log.error(
                _Exceptions.invalid_inputs,
                ", ".join(expected_inputs_keys)
            )
            exit(1)

    def launch_tool(self):
        """Function used to start the docker container with the choosed tool"""

        # Filling entrypoint with provided inputs by replacing input keys
        filtered_entrypoints = filter(lambda item: item.key == self.entrypoint,
                                      self.tool_config.entrypoints)
        selected_entrypoint = list(filtered_entrypoints)[0]
        filled_entrypoint_cmd = selected_entrypoint.command
        for index, item in enumerate(selected_entrypoint.inputs):
            cursor = f"${{{item}}}"
            value = self.inputs[index]
            filled_entrypoint_cmd = filled_entrypoint_cmd.replace(
                cursor,
                value
            )

        # Starting container
        # working_dir = os.getcwd()
        # output_volume = f'{working_dir}/output/{self.tool}'
        docker = DockerServices()
        docker.build_image(f'./tools/{self.tool}')
        docker.run_tool_container(name=self.tool,
                                  output_volume='output_data',
                                  entrypoint=filled_entrypoint_cmd)

        docker.run_logstash_container(tool=self.tool)
