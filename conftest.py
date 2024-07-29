import pytest

from pybrainuz.app import PyBrainApp


@pytest.fixture
def app():
    return PyBrainApp()


@pytest.fixture
def test_client(app):
    return app.test_session()
