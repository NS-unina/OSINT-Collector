"""
Module containing methods to properly manage docker images and containers
"""

import os
import logging
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
    _logstash_container = None

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

            self._logstash_container = self._client.containers.run(
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

        except (docker.errors.ContainerError,
                docker.errors.ImageNotFound,
                docker.errors.APIError) as e:
            self._log.error(e)
            exit(1)

    def stop_logstash_container(self):
        """
        Stop the logstash container
        """
        self._logstash_container.stop()
