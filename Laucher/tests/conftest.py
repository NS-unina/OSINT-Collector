import pytest
from app import create_app
from app.utils.services.docker_service import DockerServices


@pytest.fixture()
def app():
    app = create_app("app.configuration.TestingConfig")
    yield app


@pytest.fixture()
def app_context(app):
    """Push an application context for tests that require current_app."""
    with app.app_context():
        yield


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
