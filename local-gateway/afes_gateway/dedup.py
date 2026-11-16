"""Bounded deduplication cache keyed by (device_id, message_id)."""

from __future__ import annotations

from collections import OrderedDict


class DeduplicationCache:
    """LRU-bounded set of seen (device_id, message_id) tuples."""

    def __init__(self, max_size: int = 1024) -> None:
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self._max_size = max_size
        self._seen: OrderedDict[tuple[str, str], None] = OrderedDict()

    def seen_or_add(self, device_id: str, message_id: str) -> bool:
        """Return True if already seen; otherwise record it and return False."""
        key = (device_id, message_id)
        if key in self._seen:
            self._seen.move_to_end(key)
            return True
        self._seen[key] = None
        if len(self._seen) > self._max_size:
            self._seen.popitem(last=False)
        return False

    def __len__(self) -> int:
        return len(self._seen)
