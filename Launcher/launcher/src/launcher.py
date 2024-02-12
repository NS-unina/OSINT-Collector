"""
The module is responsible for handling the startup of the tool and
manage it's output and lifecycle
"""

import logging
import time
import os
import json
import requests
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

    output_not_found = "Logstash output not found!"

    output_upload_failed = "Logstash output upload failed, status code: %s"


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

        docker = DockerServices()
        docker.build_image(f'./tools/{self.tool}')
        docker.run_tool_container(name=self.tool,
                                  output_volume='output_data',
                                  entrypoint=filled_entrypoint_cmd)

        return True

    def generate_output(self):
        """Function used to start logstash pipeline """
        docker = DockerServices()
        docker.run_logstash_container(tool=self.tool)

        file_to_find = f"/app/output/{self.tool}-logstash.json"
        timeout_seconds = 180

        self._log.info('Waiting for output...')

        output_found = self.wait_for_file(file_to_find, timeout_seconds)

        if output_found:
            self._log.info('Logstash output generated')
        else:
            self._log.error(_Exceptions.output_not_found)

        time.sleep(5)
        docker.stop_logstash_container()

        return output_found

    def upload_output(self):
        """Function used to upload output data"""

        json_file_path = f"/app/output/{self.tool}-logstash.json"
        url = f"http://host.docker.internal:8080/results/logstash/{self.tool}"

        # Read the content of the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_content = json.load(file)

        # Send the content of the JSON file over POST request
        response = requests.post(url, json=json_content, timeout=120)

        # Clear logstash output
        self._log.info('Cleaning...')
        os.remove(json_file_path)
        self._log.info('Logstash output cleaned!')

        # Manage response
        if response.status_code == 200:
            self._log.info('Logstash output uploaded!')
        else:
            self._log.error(_Exceptions.output_upload_failed,
                            response.status_code)

        return response.status_code == 200

    def wait_for_file(self, filename, timeout=60):
        """
        Wait until the specified file exists or until the timeout (in seconds)
        is reached.

        Args:
            filename (str): The name of the file to wait for.
            timeout (int): The maximum time (in seconds) to wait for the file.
            Default is 60 seconds.

        Returns:
            bool: True if the file is found within the timeout period, False
            otherwise.
        """

        start_time = time.time()
        while not os.path.exists(filename):
            if time.time() - start_time >= timeout:
                return False  # Timeout reached
            time.sleep(1)  # Wait for 1 second
        return True
