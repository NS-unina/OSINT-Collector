import pytest
from app import create_app


@pytest.fixture()
def app():
    app = create_app("app.configuration.TestingConfig")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()