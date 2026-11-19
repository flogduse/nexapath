"""API-level tests: session isolation and input validation.

These run against the real Flask app (real TF-IDF matcher) but never touch the
network, so they are safe in CI.
"""
from __future__ import annotations

import pytest

from app import app as flask_app


@pytest.fixture()
def client():
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as c:
        yield c


def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_chat_requires_message(client):
    assert client.post("/api/chat", json={}).status_code == 400
    assert client.post("/api/chat", json={}).status_code == 400


def test_two_sessions_do_not_share_state(client):
    alice = client.post(
        "/api/chat", json={"message": "I know Python"}, headers={"X-Session-Id": "alice"}
    ).get_json()
    bob = client.post(
        "/api/chat", json={"message": "I know Java"}, headers={"X-Session-Id": "bob"}
    ).get_json()

    assert "python" in [s.lower() for s in alice["state"]["skills"]]
    assert "java" in [s.lower() for s in bob["state"]["skills"]]
    assert "python" not in [s.lower() for s in bob["state"]["skills"]]


def test_reset_only_clears_the_callers_session(client):
    client.post(
        "/api/chat", json={"message": "I know Python"}, headers={"X-Session-Id": "a"}
    )
    client.post(
        "/api/chat", json={"message": "I know Java"}, headers={"X-Session-Id": "b"}
    )

    reset = client.post("/api/chat/reset", headers={"X-Session-Id": "a"})
    assert reset.status_code == 200

    a_log = client.get("/api/chat/history", headers={"X-Session-Id": "a"}).get_json()
    b_log = client.get("/api/chat/history", headers={"X-Session-Id": "b"}).get_json()
    assert a_log["log"] == []
    assert len(b_log["log"]) == 2


def test_session_id_is_generated_and_echoed_when_absent(client):
    resp = client.post("/api/chat", json={"message": "hello"})
    assert resp.status_code == 200
    assert resp.headers.get("X-Session-Id")
