import pytest
from pytest_mock import MockFixture
from api.index import create_app_for_test

@pytest.fixture()
def app():
    app = create_app_for_test("asdasd")
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_homepage(client):
    response = client.get("api/")
    assert response.status_code == 200
    assert b"G1" in response.data

def test_longpoll(client):
    response = client.get("/longpoll")
    assert response.status_code == 200
    assert b"False" in response.data