"""
Classroom Web API - Error Guardians and Exception Handlers
Provides 400 Validation Error, 404 Reason Guardian, and HTML error templates.
"""

from fastapi import Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from middlewares.logger import log_error_to_file


def render_404_page(reason: str, path: str) -> str:
    """Renders a generic, polished 404 HTML error page with a specified reason"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>404 - Page Not Found • Alumni OS</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #090d16;
            --card-bg: rgba(15, 23, 42, 0.8);
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #f43f5e;
            --primary: #6366f1;
            --border: rgba(255, 255, 255, 0.08);
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            background-image: radial-gradient(circle at 50% 30%, rgba(244, 63, 94, 0.1) 0%, transparent 60%);
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 2.5rem;
            max-width: 540px;
            width: 100%;
            text-align: center;
            backdrop-filter: blur(16px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5);
        }}
        .badge {{
            display: inline-block;
            background: rgba(244, 63, 94, 0.15);
            color: var(--accent);
            padding: 0.35rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 1rem;
            border: 1px solid rgba(244, 63, 94, 0.3);
        }}
        h1 {{
            font-size: 3.5rem;
            line-height: 1;
            margin-bottom: 0.75rem;
            background: linear-gradient(to right, #f43f5e, #fb7185);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        h2 {{
            font-size: 1.35rem;
            margin-bottom: 1rem;
            color: #ffffff;
        }}
        .path {{
            font-family: monospace;
            background: rgba(15, 23, 42, 0.6);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            color: #38bdf8;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 1.25rem;
            word-break: break-all;
        }}
        p.reason {{
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 2rem;
        }}
        .actions {{
            display: flex;
            gap: 1rem;
            justify-content: center;
        }}
        a.btn {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            text-decoration: none;
            transition: opacity 0.2s;
            font-size: 0.9rem;
        }}
        a.btn-primary {{
            background: var(--primary);
            color: white;
        }}
        a.btn-alt {{
            background: #334155;
            color: #f8fafc;
        }}
        a.btn:hover {{ opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">404 GUARDIAN</span>
        <h1>404</h1>
        <h2>Resource or Page Not Found</h2>
        <div class="path">{path}</div>
        <p class="reason"><strong>Reason:</strong> {reason}</p>
        <div class="actions">
            <a href="/" class="btn btn-primary">Return to Hub</a>
            <a href="/api/swagger" class="btn btn-alt">Open Swagger Docs</a>
        </div>
    </div>
</body>
</html>"""


def render_500_page(reason: str, path: str) -> str:
    """Renders a safe generic 500 HTML error page with a specified reason"""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>500 - Internal Server Error</title>
    <style>
        :root {{
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text: #f8fafc;
            --muted: #94a3b8;
            --accent: #eab308;
            --primary: #4f46e5;
            --border: #334155;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2.5rem;
            max-width: 540px;
            width: 100%;
            text-align: center;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
        }}
        .badge {{
            display: inline-block;
            background: rgba(234, 179, 8, 0.15);
            color: var(--accent);
            padding: 0.35rem 0.8rem;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }}
        h1 {{
            font-size: 3.5rem;
            line-height: 1;
            margin-bottom: 0.75rem;
            background: linear-gradient(to right, #eab308, #facc15);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        h2 {{ font-size: 1.35rem; margin-bottom: 1rem; color: #ffffff; }}
        .path {{
            font-family: monospace;
            background: rgba(15, 23, 42, 0.6);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            color: #38bdf8;
            font-size: 0.9rem;
            display: inline-block;
            margin-bottom: 1.25rem;
        }}
        p.reason {{ color: var(--muted); font-size: 0.95rem; line-height: 1.6; margin-bottom: 2rem; }}
        a.btn {{
            display: inline-block;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            background: var(--primary);
            color: white;
            font-weight: 600;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="card">
        <span class="badge">5xx GUARDIAN</span>
        <h1>500</h1>
        <h2>Internal Server Error</h2>
        <div class="path">{path}</div>
        <p class="reason"><strong>Reason:</strong> {reason} The incident has been safely caught and recorded in <code>logs/error.logs</code>.</p>
        <a href="/" class="btn">Return to Safe Hub</a>
    </div>
</body>
</html>"""


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Catches Pydantic / FastAPI schema validation failures,
    returns HTTP 400 Bad Request with 'validation failed' and logs to logs/error.logs
    """
    errors_summary = exc.errors()
    error_msg = f"Validation failed on {request.method} {request.url.path}: {errors_summary}"
    log_error_to_file(error_msg, request, status_code=400)
    
    return JSONResponse(
        status_code=400,
        content={
            "error": "validation failed",
            "reason": "Request body validation failed against schema rules",
            "detail": errors_summary,
            "status_code": 400
        }
    )


async def custom_starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Intercepts Starlette HTTP exceptions including 404 Not Found with explicit reason.
    """
    if exc.status_code == 404:
        reason = exc.detail if (exc.detail and exc.detail != "Not Found") else "The requested URL route or entity does not exist on this server."
        log_error_to_file(f"404 Not Found: {reason}", request, status_code=404)
        
        accept = request.headers.get("accept", "")
        is_api = request.url.path.startswith("/api/")
        
        if "text/html" in accept and not is_api:
            return HTMLResponse(
                status_code=404,
                content=render_404_page(reason=reason, path=request.url.path)
            )
            
        return JSONResponse(
            status_code=404,
            content={
                "error": "Not Found",
                "status_code": 404,
                "reason": reason,
                "path": request.url.path
            }
        )
        
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "status_code": exc.status_code,
            "reason": exc.detail,
            "detail": exc.detail,
            "path": request.url.path
        }
    )
