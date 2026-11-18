"""
Middlewares package for Classroom Web API
"""

from middlewares.pipeline import (
    BodyCheckMiddleware,
    LoggerMiddleware,
    Guardian5xxMiddleware,
)
from middlewares.handlers import (
    validation_exception_handler,
    custom_starlette_http_exception_handler,
    render_404_page,
    render_500_page,
)
from middlewares.logger import log_terminal_request, log_error_to_file

__all__ = [
    "BodyCheckMiddleware",
    "LoggerMiddleware",
    "Guardian5xxMiddleware",
    "validation_exception_handler",
    "custom_starlette_http_exception_handler",
    "render_404_page",
    "render_500_page",
    "log_terminal_request",
    "log_error_to_file",
]
