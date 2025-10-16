import pytest
from unittest.mock import MagicMock, patch
from app.utils.services.docker_service import DockerServices


class TestDockerServices:
    """Unit tests for DockerServices class."""


    @pytest.fixture(autouse=True)
    def setup_service(self):
        """Setup a DockerServices instance with a mocked client before each test."""
        self.service = DockerServices()
        self.service._client = MagicMock()


    def test_build_image_success(self):
        """Ensure build_image calls docker.images.build correctly."""
        self.service.build_image("/tmp/test", "my-image:latest")

        self.service._client.images.build.assert_called_once_with(
            path="/tmp/test",
            tag="my-image:latest",
            dockerfile="Dockerfile",
            rm=True,
        )


    def test_build_image_logs_exception(self, caplog):
        """Ensure build_image logs exceptions properly."""
        with patch("docker.errors.BuildError", Exception):
            self.service._client.images.build.side_effect = Exception("Build failed")

            self.service.build_image("/tmp/test", "broken-image")

            assert "Unexpected error during build of broken-image" in caplog.text


    def test_pull_image_success(self):
        """Ensure pull_image calls docker.images.pull correctly."""
        self.service.pull_image("alpine:latest")

        self.service._client.images.pull.assert_called_once_with("alpine:latest")

    def test_pull_image_api_error(self, caplog):
        """Ensure pull_image logs and re-raises API errors."""
        with patch("docker.errors.APIError", Exception):
            self.service._client.images.pull.side_effect = Exception("Pull failed")

            with pytest.raises(Exception):
                self.service.pull_image("missing-image")

            assert "Docker API error while pulling missing-image" in caplog.text


    def test_run_tool_container_success(self):
        """Ensure run_tool_container correctly runs and removes images."""
        self.service.run_tool_container("alpine:latest", "output", "echo hello")

        self.service._client.containers.run.assert_called_once_with(
            image="alpine:latest",
            entrypoint="echo hello",
            volumes=["output:/output"],
            auto_remove=True,
        )
        self.service._client.images.remove.assert_called_once_with(
            image="alpine:latest", force=True
        )


    def test_run_tool_container_error_logs_and_removes_image(self, caplog):
        """Ensure container errors are logged and image is force-removed."""
        with patch("docker.errors.ContainerError", Exception):
            self.service._client.containers.run.side_effect = Exception("Run failed")

            self.service.run_tool_container("bad-image", "out", "cmd")

            assert "Docker error during run of bad-image container" in caplog.text
            self.service._client.images.remove.assert_called_with(
                image="bad-image", force=True
            )
