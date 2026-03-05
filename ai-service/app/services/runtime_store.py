from __future__ import annotations

from collections import deque
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Dict, List, Optional


class RuntimeStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._results: deque[Dict[str, Any]] = deque(maxlen=100)

    def add_result(self, payload: Dict[str, Any]) -> None:
        with self._lock:
            self._results.appendleft({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "payload": payload,
            })

    def latest(self) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._results[0] if self._results else None

    def list_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._results)[:limit]

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "total_results": len(self._results),
                "latest_timestamp": self._results[0]["timestamp"] if self._results else None,
            }


runtime_store = RuntimeStore()
