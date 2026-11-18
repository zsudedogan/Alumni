"""
Classroom Web API - Logging Utility
Manages logging to console and files (logs/error.logs and logs/requests.log).
"""

import os
from datetime import datetime
from typing import Optional
from starlette.requests import Request

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.logs")
REQUEST_LOG_FILE = os.path.join(LOG_DIR, "requests.log")


def ensure_log_dir():
    """Ensure logs directory exists"""
    os.makedirs(LOG_DIR, exist_ok=True)


def log_terminal_request(time_str: str, method: str, route: str, status_code: int, duration_ms: int):
    """
    Format requested: [time] [method] [route] [res.type] [duration]
    Example: 10:20:30 Post /users/1/json 201 18ms
    """
    formatted_method = method.capitalize()
    log_line = f"{time_str} {formatted_method} {route} {status_code} {duration_ms}ms"
    print(log_line)
    
    # Also append to requests.log
    try:
        ensure_log_dir()
        with open(REQUEST_LOG_FILE, "a", encoding="utf-8") as f:
            now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now_iso}] {log_line}\n")
    except Exception:
        pass


def log_error_to_file(error_detail: str, request: Optional[Request] = None, status_code: int = 500):
    """
    Persists error records to logs/error.logs
    """
    try:
        ensure_log_dir()
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        method = request.method if request else "SYSTEM"
        path = request.url.path if request else "N/A"
        
        log_entry = (
            f"[{now_str}] [{method} {path}] Status: {status_code}\n"
            f"Detail: {error_detail}\n"
            f"{'-' * 60}\n"
        )
        
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
        # Also write to error.log as standard alias
        alt_log = os.path.join(LOG_DIR, "error.log")
        with open(alt_log, "a", encoding="utf-8") as f:
            f.write(log_entry)
    except Exception as e:
        print(f"Failed to write to error log: {e}")
