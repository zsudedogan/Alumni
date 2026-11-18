"""
Classroom Web API - Middleware Pipeline Architecture
Ordered Pipeline: Request -> Guardian 5xx -> Logger -> Read JSON (Body Check) -> Route / Action
"""

import json
import time
import traceback
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, HTMLResponse, Response
from middlewares.logger import log_terminal_request, log_error_to_file
from middlewares.handlers import render_500_page


class BodyCheckMiddleware(BaseHTTPMiddleware):
    """
    Step 3 in Pipeline: Read JSON (Body Check)
    Inspects incoming POST, PUT, and PATCH requests for valid JSON syntax.
    If malformed or invalid, catches the error and returns 400 'validation failed'.
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method in ("POST", "PUT", "PATCH"):
            content_type = request.headers.get("content-type", "").lower()
            if "application/json" in content_type:
                try:
                    # Read raw body bytes
                    body = await request.body()
                    if body:
                        # Attempt parsing JSON
                        try:
                            json.loads(body)
                        except json.JSONDecodeError as jde:
                            err_msg = f"Invalid JSON body: {jde.msg} at line {jde.lineno} col {jde.colno}"
                            log_error_to_file(err_msg, request, status_code=400)
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "error": "validation failed",
                                    "reason": "Malformed or invalid JSON body payload",
                                    "detail": err_msg,
                                    "status_code": 400
                                }
                            )
                except Exception as e:
                    err_msg = f"Error reading request body: {str(e)}"
                    log_error_to_file(err_msg, request, status_code=400)
                    return JSONResponse(
                        status_code=400,
                        content={
                            "error": "validation failed",
                            "reason": "Could not read request body",
                            "detail": str(e),
                            "status_code": 400
                        }
                    )

        return await call_next(request)


class LoggerMiddleware(BaseHTTPMiddleware):
    """
    Step 2 in Pipeline: Logger Middleware
    Logs every request to terminal in format:
    [time] [method] [route] [res.type] [duration]
    Example: 10:20:30 Post /users/1/json 201 18ms
    Persists error records to logs/error.logs
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.perf_counter()
        time_str = datetime.now().strftime("%H:%M:%S")

        try:
            response = await call_next(request)
        except Exception:
            # Let Guardian5xxMiddleware handle exception, but re-raise after calculating
            duration_ms = max(1, int((time.perf_counter() - start_time) * 1000))
            log_terminal_request(time_str, request.method, request.url.path, 500, duration_ms)
            raise

        duration_ms = max(1, int((time.perf_counter() - start_time) * 1000))
        log_terminal_request(time_str, request.method, request.url.path, response.status_code, duration_ms)

        # If HTTP error status (4xx or 5xx), log to error.logs if not already logged
        if response.status_code >= 400:
            log_error_to_file(
                f"HTTP {response.status_code} on {request.method} {request.url.path} (Duration: {duration_ms}ms)",
                request,
                status_code=response.status_code
            )

        return response


class Guardian5xxMiddleware(BaseHTTPMiddleware):
    """
    Step 1 in Pipeline (Guardian Envelope): 5xx Guardian
    Catches unhandled server exceptions, logs full traceback to logs/error.logs,
    and returns a clean, safe 500 response (JSON for API, HTML for Web).
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            return await call_next(request)
        except Exception as exc:
            tb = traceback.format_exc()
            error_msg = f"Unhandled Exception: {str(exc)}\n{tb}"
            log_error_to_file(error_msg, request, status_code=500)

            # Check if API or Web UI
            accept = request.headers.get("accept", "")
            is_api = request.url.path.startswith("/api/")

            if "text/html" in accept and not is_api:
                return HTMLResponse(
                    status_code=500,
                    content=render_500_page(
                        reason="An unexpected internal server error was intercepted by 5xx Guardian.",
                        path=request.url.path
                    )
                )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "status_code": 500,
                    "reason": "An unexpected server error occurred. Intercepted by Guardian Middleware.",
                    "path": request.url.path
                }
            )
