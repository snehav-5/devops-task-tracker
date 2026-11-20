import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from app import create_app  # noqa: E402


@pytest.fixture()
def client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_add_and_list_task(client):
    client.post("/add", data={"title": "Learn Docker"})
    res = client.get("/api/tasks")
    assert res.get_json()[0]["title"] == "Learn Docker"


def test_toggle_task(client):
    client.post("/add", data={"title": "Write CI/CD"})
    client.get("/toggle/1")
    assert client.get("/api/tasks").get_json()[0]["done"] is True


def test_delete_task(client):
    client.post("/add", data={"title": "Temp"})
    client.get("/delete/1")
    assert client.get("/api/tasks").get_json() == []
