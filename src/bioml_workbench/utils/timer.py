from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Iterator, Literal


@dataclass(frozen=True)
class Timer:
    """A timer for measuring block execution time."""

    start_time: float = 0.0
    end_time: float = 0.0

    def elapsed(self) -> float:
        """Return the elapsed time in seconds."""

        return max(0.0, self.end_time - self.start_time)


class TimerContext:
    """Context manager for timing a code block."""

    def __init__(self, label: str | None = None) -> None:
        self.label = label
        self.timer = Timer()

    def __enter__(self) -> Timer:
        self.timer = Timer(start_time=time.perf_counter(), end_time=0.0)
        return self.timer

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> Literal[False]:
        object.__setattr__(self.timer, "end_time", time.perf_counter())
        return False


@contextmanager
def timed_section(label: str | None = None) -> Iterator[Timer]:
    """Context manager that returns timing information."""

    timer = Timer(start_time=time.perf_counter(), end_time=0.0)
    try:
        yield timer
    finally:
        object.__setattr__(timer, "end_time", time.perf_counter())
