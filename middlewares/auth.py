"""
Authentication & Authorization Middleware - MVC Architecture
Manages session cookies, Bearer tokens, user identity injection, and Role-Based Access Control (RBAC).
Protects administrative paths (/admin/* and /api/admin/*) ensuring only users with role='Admin' can access.
"""

import uuid
import secrets
from typing import Optional, Dict
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse, RedirectResponse, HTMLResponse
from models.user import get_user_record_by_id, User

# In-memory session store mapping session_token -> user_id
_ACTIVE_SESSIONS: Dict[str, int] = {}


def create_user_session(user_id: int) -> str:
    """Generates a secure session token and registers the user session"""
    token = f"sess_{secrets.token_urlsafe(32)}"
    _ACTIVE_SESSIONS[token] = user_id
    return token


def get_user_from_token(token: Optional[str]) -> Optional[User]:
    """Retrieves the User model instance associated with a session token"""
    if not token or token not in _ACTIVE_SESSIONS:
        return None
    user_id = _ACTIVE_SESSIONS[token]
    user = get_user_record_by_id(user_id)
    if not user:
        # Invalid user, cleanup token
        _ACTIVE_SESSIONS.pop(token, None)
        return None
    return user


def destroy_user_session(token: Optional[str]) -> bool:
    """Terminates an active session token"""
    if token and token in _ACTIVE_SESSIONS:
        del _ACTIVE_SESSIONS[token]
        return True
    return False


def get_current_user_from_request(request: Request) -> Optional[User]:
    """Helper to extract user from request cookies or Authorization header"""
    # 1. Check Cookie
    token = request.cookies.get("session_token")
    if token:
        user = get_user_from_token(token)
        if user:
            return user

    # 2. Check Authorization header: Bearer <token>
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.replace("Bearer ", "").strip()
        user = get_user_from_token(token)
        if user:
            return user

    return None


def render_403_page(user_name: str, role: str) -> str:
    """Renders UniBridge styled 403 Forbidden page for unauthorized admin access"""
    from views.components import get_base_css, render_navbar, render_footer
    return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>403 Yetkisiz Erişim • UniBridge</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        {get_base_css()}
        .forbidden-card {{
            max-width: 620px;
            margin: 4rem auto;
            background: var(--bg-surface);
            border: 1px solid rgba(239, 68, 68, 0.3);
            border-radius: var(--radius-card);
            padding: 3rem 2.5rem;
            text-align: center;
            box-shadow: 0 10px 30px rgba(239, 68, 68, 0.08);
        }}
        .forbidden-icon {{
            font-size: 3.5rem;
            margin-bottom: 1rem;
        }}
        .forbidden-badge {{
            display: inline-block;
            background: #fee2e2;
            color: #b91c1c;
            padding: 0.35rem 1rem;
            border-radius: 9999px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-bottom: 1rem;
        }}
    </style>
</head>
<body>
    {render_navbar(active_route="admin")}
    <main class="container">
        <div class="forbidden-card">
            <div class="forbidden-icon">🛡️</div>
            <div class="forbidden-badge">HTTP 403 FORBIDDEN</div>
            <h1 style="color: #991b1b; font-size: 1.8rem; margin-bottom: 0.75rem;">Yönetici Yetkisi Gerekli</h1>
            <p style="color: var(--text-muted); margin-bottom: 1.5rem; line-height: 1.6;">
                Merhaba <strong>{user_name}</strong>. Mevcut rolünüz (<strong>{role}</strong>) yönetim paneline erişim için yeterli değildir.
                Bu alana yalnızca <strong>Admin</strong> yetkisine sahip kullanıcılar erişebilir.
            </p>
            <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                <a href="/" class="btn btn-primary">Ana Sayfaya Dön</a>
                <a href="/logout/" class="btn btn-secondary">Farklı Hesapla Giriş Yap</a>
            </div>
        </div>
    </main>
    {render_footer()}
</body>
</html>"""


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Authentication & Role-Based Access Control Middleware.
    Inspects session token from Cookie or Authorization header.
    Injects request.state.user.
    Enforces Admin role for /admin and /api/admin endpoints.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        path = request.url.path
        current_user = get_current_user_from_request(request)
        request.state.user = current_user

        # Check if the requested route is under Admin control
        is_admin_route = path == "/admin" or path.startswith("/admin/") or path.startswith("/api/admin")

        if is_admin_route:
            # 1. Unauthenticated Check
            if not current_user:
                accept_header = request.headers.get("accept", "")
                is_html_request = "text/html" in accept_header and not path.startswith("/api/")
                if is_html_request:
                    login_url = f"/login/?next={path}&error=auth_required"
                    return RedirectResponse(url=login_url, status_code=303)
                return JSONResponse(
                    status_code=401,
                    content={
                        "error": "Unauthorized",
                        "detail": "Authentication required. Please log in to access administrative resources.",
                        "status_code": 401,
                        "path": path,
                    }
                )

            # 2. Role Authorization Check: Must have Admin role
            if current_user.role != "Admin":
                accept_header = request.headers.get("accept", "")
                is_html_request = "text/html" in accept_header and not path.startswith("/api/")
                if is_html_request:
                    return HTMLResponse(
                        status_code=403,
                        content=render_403_page(user_name=current_user.name, role=current_user.role)
                    )
                return JSONResponse(
                    status_code=403,
                    content={
                        "error": "Forbidden",
                        "detail": f"Admin role required. Current user role is '{current_user.role}'.",
                        "status_code": 403,
                        "path": path,
                    }
                )

        # Proceed with request pipeline
        return await call_next(request)
