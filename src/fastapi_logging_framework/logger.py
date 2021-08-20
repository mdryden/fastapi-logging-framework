from __future__ import annotations

import logging
import traceback
from typing import Dict, Optional
from starlette_context import context


class Logger:
    _instance = None
    _logger: Logger = None

    def __init__(self):
        raise RuntimeError("To change the default logger, call 'set_logger()'")

    @classmethod
    def __ensure_initialized(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._logger = DefaultLogger()

    @classmethod
    def logger_type(cls) -> str:
        return type(cls._logger).__name__

    @classmethod
    def set_logger(cls, logger: Logger):
        cls._instance = cls.__new__(cls)
        cls._logger = logger if logger else DefaultLogger()

    @classmethod
    def get_trace_id(cls) -> Optional[str]:
        return context.data['X-Request-ID'] if context.exists() else None

    @classmethod
    def debug(cls, message: str, extra: Dict = None):
        cls.__ensure_initialized()
        cls._logger.debug(message, extra)

    @classmethod
    def info(cls, message: str, extra: Dict = None):
        cls.__ensure_initialized()
        cls._logger.info(message, extra)

    @classmethod
    def warn(cls, message: str, extra: Dict = None):
        cls.__ensure_initialized()
        cls._logger.warn(message, extra)

    @classmethod
    def error(cls, message: str, exc_info=None, extra: Dict = None):
        cls.__ensure_initialized()
        formatted_exception = None

        if exc_info and isinstance(exc_info, BaseException):
            formatted_exception = traceback.format_exception(type(exc_info), exc_info, exc_info.__traceback__)
            formatted_exception = "\n".join(formatted_exception)

        cls._logger.error(message, exc_info=formatted_exception, extra=extra)


class DefaultLogger(Logger):
    def __init__(self):
        self.logger = logging.getLogger("uvicorn")

    def __log(self, level: int, message: str, extra: Dict = None):
        trace = self.get_trace_id()
        if trace:
            message = f"[{trace}] {message}"

        if extra:
            message = f"{message}\n\t\t{extra}"

        self.logger.log(level, message)

    def debug(self, message: str, extra: Dict = None):
        self.__log(logging.DEBUG, message, extra=extra)

    def info(self, message: str, extra: Dict = None):
        self.__log(logging.INFO, message, extra=extra)

    def warn(self, message: str, extra: Dict = None):
        self.__log(logging.WARN, message, extra=extra)

    def error(self, message: str, extra: Dict = None, exc_info=None):
        trace = self.get_trace_id()
        if trace:
            message = f"[{trace}] {message}"

        if extra:
            message = f"{message}\n\t\t{extra}"

        self.logger.error(message, exc_info=exc_info)
