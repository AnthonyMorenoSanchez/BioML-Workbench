import time

from bioml_workbench.utils.timer import TimerContext, timed_section


def test_timer_context_measurement() -> None:
    with TimerContext() as timer:
        time.sleep(0.01)

    assert timer.elapsed() > 0.0


def test_timed_section_context() -> None:
    with timed_section("section") as timer:
        time.sleep(0.01)

    assert timer.elapsed() > 0.0
