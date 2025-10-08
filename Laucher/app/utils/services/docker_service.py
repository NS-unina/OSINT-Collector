# Module containing methods to properly manage docker images and containers
import os
import logging
import docker


class _Exceptions:
    """
    Manage docker services errors
    """

    invalid_order = ("run_container method should be "
                     "called only after build_image method")


class DockerServices:
    """
    Class containing methods to properly manage docker images and containers
    """

    _log = logging.getLogger(__name__)
    _client = docker.from_env()


    def build_image(self, folder_path, tag, dockerfile = "Dockerfile"):
        """
        Build a Docker image using the Dockerfile provided in the
        specified folder.

        Args:
            folder_path (str): The path to the folder containing
            the Dockerfile.
            tag (str): Image tag to assign.
            dockerfile (str, optional): Name of the Dockerfile to use. 
            Defaults to 'Dockerfile'.
        """
        
        self._log.info('Building Dockerfile image in %s', folder_path)

        try:
            self._client.images.build(path=folder_path,
                                      tag=tag,
                                      dockerfile=dockerfile,
                                      rm=True)

        except (docker.errors.BuildError,
                docker.errors.APIError,
                TypeError) as e:
            self._log.exception("Unexpected error during build of %s: %s", tag, str(e))


    def pull_image(self, tag):
        """
        Pull a Docker image from the registry.

        Args:
            tag (str): The full image tag.
        """
        
        self._log.info("Pulling image Dockerfile image in %s", tag)
        
        try:
            self._client.images.pull(tag)
        except (docker.errors.APIError) as e:
            self._log.error("Docker API error while pulling %s: %s", tag, str(e))


    def run_tool_container(self, name, output_volume, entrypoint):
        """
        Run a Docker container with the provided image.

        TODO: DA MODIFICARE

        Args:
            name (str): The name of the container.
            output_volume (str): The name of the volume to mount for output.
            entrypoint (str): The entry point command to run within
                              the container.
        """

        if self._image_tag is None:
            self._log.error(_Exceptions.invalid_order)

        self._log.info('Running %s container', name)
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

        self._client.images.remove(image=self._image_tag, force=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    docker_engine = DockerServices()
    docker_engine.pull_image("osintcollector/snscrape:latest")
    print("ciao")
    