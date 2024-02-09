"""
Module containing methods to properly manage docker images and containers
"""

import os
import logging
import time
import docker


class _Exceptions:
    """Manage docker services errors"""

    invalid_order = ("run_container method should be "
                     "called only after build_image method")


class DockerServices:
    """
    Class containing methods to properly manage docker images and containers
    """

    _client = docker.from_env()
    _log = logging.getLogger(__name__)
    _image_tag = None

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

    def build_image(self, folder_path):
        """
        Build the docker image for the Dockerfile provided into the
        folder_path folder
        """

        self._log.info('Building image...')
        tag = os.path.basename(folder_path)

        try:
            self._client.images.build(path=folder_path,
                                      tag=tag,
                                      dockerfile='Dockerfile')

        except (docker.errors.BuildError,
                docker.errors.APIError,
                TypeError) as e:
            self._log.error(e)
            exit(1)

        self._image_tag = tag

    def run_tool_container(self, name, output_volume, entrypoint):
        """
        Run a docker container with the provided image
        """

        if self._image_tag is None:
            self._log.error(_Exceptions.invalid_order)
            exit(1)

        self._log.info('Running container...')
        try:

            self._client.containers.run(image=self._image_tag,
                                        name=name,
                                        entrypoint=entrypoint,
                                        volumes=[f'{output_volume}:/output'],
                                        auto_remove=True)

        except (docker.errors.ContainerError,
                docker.errors.ImageNotFound,
                docker.errors.APIError) as e:
            self._log.error(e)
            self._client.images.remove(image=self._image_tag, force=True)
            exit(1)

        self._client.images.remove(image=self._image_tag, force=True)

    def run_logstash_container(self, tool):
        """
        Run a logstash container for the provided tool
        """

        self._log.info('Running logstash...')

        image_name = "docker.elastic.co/logstash/logstash:8.12.0"
        container_name = "logstash"
        output_vol = "output_data:/output"
        tools_vol = "tools_conf:/tools_conf"
        command = f'logstash -f /tools_conf/{tool}.conf -w 1'

        try:

            _logstash_container = self._client.containers.run(
                image=image_name,
                name=container_name,
                command=command,
                user="root",
                auto_remove=True,
                detach=True,
                ports={
                    '5044': '5044',
                    '9600': '9600'
                },
                environment={
                    'xpack.monitoring.enabled': 'false',
                    'log.level': 'info'
                },
                volumes=[
                    output_vol,
                    tools_vol
                ],

            )

            file_to_find = "/app/output/logstash.json"
            timeout_seconds = 180

            self._log.info('Waiting for output...')
            if self.wait_for_file(file_to_find, timeout_seconds):
                self._log.info('Logstash output generated')
            else:
                self._log.error('Logstash output not found!')

            time.sleep(5)
            _logstash_container.stop()

        except (docker.errors.ContainerError,
                docker.errors.ImageNotFound,
                docker.errors.APIError) as e:
            self._log.error(e)
            exit(1)
