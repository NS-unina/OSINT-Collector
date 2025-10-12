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


@pytest.fixture
def example_tool_dict():
    """Provide an example tool dictionary structure."""
    return {
        "snscrape": {
            "description": "Download telegram data",
            "image": "snscrape/image:latest",
            "entrypoints": [
                {
                    "feature_key": "download-messages",
                    "name": "Download messages",
                    "description": "Download Telegram messages",
                    "command": "snscrape --max-results ${RESULTS} telegram-channel ${CHANNEL}",
                    "inputs": ["CHANNEL", "RESULTS"],
                }
            ],
            "inputs": [
                {"input_key": "CHANNEL", "description": "Telegram channel", "type": "string"},
                {"input_key": "RESULTS", "description": "Number of results", "type": "int"},
            ],
        }
    }
