import logging

import pytest

from bioml_workbench.utils.exceptions import handle_exceptions


def test_handle_exceptions_logs_and_reraises(caplog) -> None:
    logger = logging.getLogger("bioml_test")
    with pytest.raises(ValueError):
        with handle_exceptions(logger, "failure occurred"):
            raise ValueError("bad state")

    assert "failure occurred" in caplog.text
    assert "bad state" in caplog.text
