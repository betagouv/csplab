import threading
import time


class RateLimiter:
    """Ensures callers of wait() are spaced by at least 1 / max_calls_per_second."""

    def __init__(self, max_calls_per_second: float) -> None:
        self._min_interval = 1.0 / max_calls_per_second
        self._lock = threading.Lock()
        self._last_call: float | None = None

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            if self._last_call is not None:
                remaining = self._min_interval - (now - self._last_call)
                if remaining > 0:
                    time.sleep(remaining)
            self._last_call = time.monotonic()
