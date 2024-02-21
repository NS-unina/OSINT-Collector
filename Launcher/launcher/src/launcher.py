"""
The module is responsible for handling the startup of the tool and
manage it's output and lifecycle
"""

import logging
import time
import os
import json
import requests
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

    output_upload_failed = ("Logstash output upload failed, last failed"
                            "request respond with status code: %s,"
                            "the request sent was: %s")


class Launcher:
    """
    Class responsible for handling the startup of the tool and
    manage it's output and lifecycle
    """

    _log = logging.getLogger(__name__)

    def __init__(self, tool: str, entrypoint: str, inputs: [str]):
        """
        Initialize the launcher with the provided values.

        Args:
            tool (str): The name of the tool.
            entrypoint (str): The entry point of the tool.
            inputs ([str]): List of inputs for the tool.
        """
        self.tool = tool
        self.entrypoint = entrypoint
        self.inputs = inputs
        self.tool_config = YAMLServices.read_tool_config(self.tool)

    def launch_tool(self):
        """
        Function used to start the Docker container with the chosen tool.

        This method fills the entry point with provided inputs by replacing
        input keys, then logs the launch information, builds the Docker
        image, and runs the tool container.

        Returns:
            bool: True if the tool is successfully launched, False otherwise.
        """

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

        self._log.info(
            'Launching %s with entrypoint %s',
            self.tool,
            filled_entrypoint_cmd
        )

        docker = DockerServices()
        docker.build_image(f'./tools/{self.tool}')
        docker.run_tool_container(name=self.tool,
                                  output_volume='output_data',
                                  entrypoint=filled_entrypoint_cmd)

        return True

    def generate_output(self):
        """
        Start the Logstash pipeline to generate output.

        This method starts the Logstash pipeline, waits for
        the output file to be generated, and stops the Logstash
        container afterwards.

        Returns:
            bool: True if the output file is found, False otherwise.
        """

        docker = DockerServices()
        docker.run_logstash_container(tool=self.tool)

        file_to_find = f"/app/output/{self.tool}-logstash.json"
        timeout_seconds = 60

        self._log.info('Waiting for output')

        output_found = self.wait_for_file(file_to_find, timeout_seconds)

        time.sleep(5)
        docker.stop_logstash_container()
        time.sleep(10)

        output_found = os.path.exists(file_to_find)

        if output_found:
            self._log.info('Logstash output found')
        else:
            self._log.error(_Exceptions.output_not_found)

        return output_found

    def upload_output(self):
        """
        Upload the output data to a specified URL.

        This method reads the Logstash output file, processes each JSON-like
        object found, and sends it over a POST request to the specified URL.

        Returns:
            bool: True if the upload is successful, False otherwise.
        """

        self._log.info("Reading Logstash output file")

        json_file_path = f"/app/output/{self.tool}-logstash.json"
        url = f"http://host.docker.internal:8080/logstash/{self.tool}"

        success = True
        last_failed_req = None

        json_contents = self.read_json_file(json_file_path)

        # Process each JSON-like object found
        for obj_str in json_contents:

            try:
                # Load the JSON-like object as JSON
                json_content = json.loads(obj_str)

                self._log.debug(
                    "Sending POST request with: %s",
                    json_content
                )

                # Send the content of the JSON file over POST request
                response = requests.post(
                    url,
                    json=json_content,
                    timeout=120
                )

                if response.status_code != 200:
                    success = False
                    last_failed_req = url + " " + str(json_content)

            except json.JSONDecodeError:
                self._log.error("Error decoding JSON: %s", obj_str)

        # Manage response
        if success:
            self._log.info('Logstash output uploaded!')
        else:
            self._log.error(_Exceptions.output_upload_failed,
                            response.status_code,
                            last_failed_req)

        return success

    def clear_artifacts(self):
        """
        Clean up output data.

        This method removes all files and directories within
        the output directory.
        """

        self._log.info('Cleaning')

        output_dir = "/app/output"
        for root, dirs, files in os.walk(output_dir, topdown=False):
            for file_name in files:
                # Removes each file
                file_path = os.path.join(root, file_name)
                os.remove(file_path)

            for dir_name in dirs:
                # Removes each directory
                dir_path = os.path.join(root, dir_name)
                os.rmdir(dir_path)

        self._log.info('All artifacts cleaned!')

    def wait_for_file(self, filename, timeout=60):
        """
        Wait until the specified file exists or until the timeout (in seconds)
        is reached.

        Args:
            filename (str): The name of the file to wait for.
            timeout (int): Th e maximum time (in seconds) to wait for the file.
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

    def read_json_file(self, file_path):
        """
        Read a JSON file and return its content as a list of JSON strings.

        Args:
        file_path (str): The path to the JSON file.

        Returns:
        list: A list of JSON strings.

        If the file contains a single JSON object, it will be returned
        as a list with one element.

        If the file contains multiple JSON objects separated by '}{',
        each object will be returned as a separate string in the list.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:

                json_data = ""
                for line in file.readlines():
                    line = line.strip()
                    line = line.replace("\n", "")
                    line = line.replace("\t", "")
                    json_data += line

                if '}{' not in json_data:
                    return [json_data]

                output = []
                segments = json_data.split('}{')
                for index, segment in enumerate(segments):
                    if index == 0:
                        segment += "}"
                    elif index == len(segments)-1:
                        segment = "{" + segment
                    else:
                        segment = "{" + segment + "}"

                    output.append(segment)

                return output

        except FileNotFoundError:
            self._log.error(_Exceptions.output_not_found)
            return []
