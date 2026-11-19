"""Tests for the per-session store (stdlib only, no Flask, no sklearn)."""
from __future__ import annotations

import threading
import time

import pytest

from session_store import SessionStore


def test_same_id_returns_same_object():
    store = SessionStore(dict)
    first = store.get("abc")
    first["seen"] = 1
    assert store.get("abc") is first
    assert store.get("abc")["seen"] == 1


def test_distinct_ids_are_isolated():
    store = SessionStore(dict)
    store.get("a")["who"] = "alice"
    store.get("b")["who"] = "bob"
    assert store.get("a")["who"] == "alice"
    assert store.get("b")["who"] == "bob"


def test_discard_drops_only_that_session():
    store = SessionStore(dict)
    store.get("a")
    store.get("b")
    assert store.discard("a") is True
    assert store.discard("a") is False
    assert len(store) == 1


def test_max_sessions_evicts_least_recently_used():
    store = SessionStore(dict, max_sessions=2)
    store.get("a")
    store.get("b")
    store.get("a")  # refresh a, so b is now oldest
    store.get("c")
    assert len(store) == 2
    assert store.discard("b") is False
    assert store.discard("a") is True


def test_idle_sessions_expire():
    store = SessionStore(dict, ttl_seconds=0.05)
    store.get("old")["v"] = 1
    time.sleep(0.08)
    assert store.get("old") == {}  # fresh object, old one expired


def test_invalid_configuration_rejected():
    with pytest.raises(ValueError):
        SessionStore(dict, ttl_seconds=0)
    with pytest.raises(ValueError):
        SessionStore(dict, max_sessions=0)


def test_concurrent_gets_are_thread_safe():
    store = SessionStore(dict)

    def worker(n: int) -> None:
        for i in range(200):
            store.get(f"s{i % 5}")["tick"] = n

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(store) == 5
