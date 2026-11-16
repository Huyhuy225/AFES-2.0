"""Bounded FIFO buffer for offline telemetry storage and ordered replay."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BufferedEnvelope:
    topic: str
    payload: dict[str, Any]


class BoundedReplayBuffer:
    """Stores telemetry envelopes when upstream is unavailable."""

    def __init__(self, max_size: int = 500) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._queue: deque[BufferedEnvelope] = deque()
        self.dropped_count: int = 0

    def push(self, topic: str, payload: dict[str, Any]) -> None:
        if len(self._queue) >= self._max_size:
            self._queue.popleft()
            self.dropped_count += 1
        self._queue.append(BufferedEnvelope(topic=topic, payload=payload))

    def drain_in_order(self) -> list[BufferedEnvelope]:
        items = list(self._queue)
        self._queue.clear()
        return items

    def peek_all(self) -> list[BufferedEnvelope]:
        return list(self._queue)

    def __len__(self) -> int:
        return len(self._queue)
