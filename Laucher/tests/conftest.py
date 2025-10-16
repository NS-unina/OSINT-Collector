import pytest
from app import create_app
from app.utils.services.docker_service import DockerServices


@pytest.fixture()
def app():
    """Create a Flask app instance using the testing configuration.

    Yields:
        Flask: A Flask application instance configured for testing.
    """
    app = create_app("app.configuration.TestingConfig")
    yield app


@pytest.fixture()
def client(app):
    """
    Create a test client to simulate HTTP requests without starting a server.

    Args:
        app (Flask): The Flask app instance created by the `app` fixture.

    Returns:
        FlaskClient: The test client object for sending requests to routes.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a CLI runner to test Flask command-line commands.

    Args:
        app (Flask): The Flask app instance created by the `app` fixture.

    Returns:
        FlaskCliRunner: A runner object used to invoke CLI commands in tests.
    """
    return app.test_cli_runner()
