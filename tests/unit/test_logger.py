import pytest
from src.logger import Logger

logging_methods = [
    Logger.debug,
    Logger.info,
    Logger.warn,
    Logger.error
]


@pytest.mark.parametrize("logging_method", logging_methods)
def test_default_no_exceptions(logging_method):
    logging_method("message")


def test_cannot_call_init():
    with pytest.raises(RuntimeError):
        Logger()


def test_cannot_set_null_logger():
    Logger.set_logger(None)
    assert Logger._instance is not None
