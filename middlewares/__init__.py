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
from middlewares.auth import (
    AuthMiddleware,
    create_user_session,
    get_user_from_token,
    destroy_user_session,
    get_current_user_from_request,
)

__all__ = [
    "BodyCheckMiddleware",
    "LoggerMiddleware",
    "Guardian5xxMiddleware",
    "AuthMiddleware",
    "create_user_session",
    "get_user_from_token",
    "destroy_user_session",
    "get_current_user_from_request",
    "validation_exception_handler",
    "custom_starlette_http_exception_handler",
    "render_404_page",
    "render_500_page",
    "log_terminal_request",
    "log_error_to_file",
]
