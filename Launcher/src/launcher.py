"""
The module is responsible for handling the startup of the tool and
manage it's output and lifecycle
"""

import os
import logging
from src.globals import tools
from src.services.kafka_services import KafkaServices
from src.services.yaml_services import read_tool_config
from src.services.docker_services import build_image, run_container


class LauncherException(Exception):
    """Manage launcher errors"""


class Launcher:
    """
    Class responsible for handling the startup of the tool and
    manage it's output and lifecycle
    """

    _log = logging.getLogger(__name__)

    def __init__(self, tool: str, inputs: [str]):
        """
        Initialize the launcher with the provided value

        Raises: LauncherException
        If there is an error during the initialization.
        """
        self.tool = tool
        self.inputs = inputs
        self.tool_config = read_tool_config(self.tool)

        # Check if tool is valid
        available_tools = tools()
        if self.tool not in available_tools:
            self._log.error(
                "Unknown tool, one the following tool should be provided: %s",
                ", ".join(available_tools)
            )
            raise LauncherException("Invalid Tool")

        # Check if all inputs has been provided
        tool_cfg_in = self.tool_config.inputs
        if len(tool_cfg_in) != len(inputs):
            expected_inputs_keys = map(lambda item: item.key, tool_cfg_in)

            self._log.error(
                "Wrong inputs, the following inputs should be provided: %s",
                ", ".join(expected_inputs_keys)
            )

            raise LauncherException("Invalid Inputs")

    def launch_tool(self):
        """Function used to start the docker container with the choosed tool"""

        # Filling entrypoint with provided inputs by replacing input keys
        filled_entrypoint = self.tool_config.entrypoint
        for index, item in enumerate(self.tool_config.inputs):
            cursor = f"${item.key}"
            value = self.inputs[index]
            filled_entrypoint = filled_entrypoint.replace(cursor, value)

        # Starting container
        working_dir = os.getcwd()
        image_tag = build_image(f'./tools/{self.tool}')
        run_container(image_tag=image_tag,
                      name=self.tool,
                      output_volume=f'{working_dir}/output/{self.tool}',
                      entrypoint=filled_entrypoint)

        # Managing output
        self._manage_output(self.tool)

    def _manage_output(self, tool: str):
        """Function used to manage the tool output and send data to Kafka"""

        folder_path = f'./output/{tool}'
        if not os.path.exists(folder_path):
            raise LauncherException("Output folder does not exist")

        kafka = KafkaServices()

        # Iterate through each folder and subfolder to find
        # all the .json output file
        for root, _, files in os.walk(folder_path):
            for filename in files:
                file_path = os.path.join(root, filename)

                # Check if file is a json
                if filename.lower().endswith('.json'):
                    kafka.write(file_path=file_path)
