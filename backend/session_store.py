"""Per-session agent storage for the Flask API.

Why this exists: the original app created one module-level `CareerAgent` and
every request mutated its `conversation_state`. On a long-lived server (or a
warm Vercel instance) two visitors' conversations would bleed into each other,
and `/api/chat/reset` wiped everyone's chat.

This store keeps one agent per session id with a TTL and a hard cap, using only
the standard library so it can be unit-tested without Flask or scikit-learn.
"""
from __future__ import annotations

import threading
import time
from collections import OrderedDict
from typing import Callable, Generic, TypeVar

T = TypeVar("T")

DEFAULT_TTL_SECONDS = 2 * 60 * 60   # a chat session idles out after two hours
DEFAULT_MAX_SESSIONS = 500          # protects memory on a small dyno


class SessionStore(Generic[T]):
    """Thread-safe LRU map of session_id -> object with idle expiry."""

    def __init__(
        self,
        factory: Callable[[], T],
        ttl_seconds: float = DEFAULT_TTL_SECONDS,
        max_sessions: int = DEFAULT_MAX_SESSIONS,
    ) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be positive")
        if max_sessions < 1:
            raise ValueError("max_sessions must be at least 1")
        self._factory = factory
        self._ttl = ttl_seconds
        self._max = max_sessions
        self._items: OrderedDict[str, tuple[T, float]] = OrderedDict()
        self._lock = threading.Lock()

    def get(self, session_id: str) -> T:
        """Return the session's object, creating and refreshing it as needed."""
        now = time.monotonic()
        with self._lock:
            self._prune(now)
            found = self._items.get(session_id)
            if found is not None:
                value, _ = found
                self._items.move_to_end(session_id)
                self._items[session_id] = (value, now)
                return value
            value = self._factory()
            self._items[session_id] = (value, now)
            while len(self._items) > self._max:
                self._items.popitem(last=False)
            return value

    def discard(self, session_id: str) -> bool:
        """Drop one session; returns whether it existed."""
        with self._lock:
            return self._items.pop(session_id, None) is not None

    def __len__(self) -> int:
        with self._lock:
            return len(self._items)

    def _prune(self, now: float) -> None:
        while self._items:
            _, (_, seen) = next(iter(self._items.items()))
            if now - seen <= self._ttl:
                break
            self._items.popitem(last=False)
