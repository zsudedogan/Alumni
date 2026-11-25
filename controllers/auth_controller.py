"""
Auth Controller - MVC Architecture
Handles Authentication HTTP requests: Web Login View, API Login, Logout, and Session Verification.
"""

from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Request, Response, Form, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from models.user import authenticate_user, User
from middlewares.auth import (
    create_user_session,
    destroy_user_session,
    get_current_user_from_request,
)
from views.login_view import render_login_page

auth_router = APIRouter(tags=["Authentication & Registration"])


class LoginRequest(BaseModel):
    """Schema for JSON API login"""
    email: str
    password: str


# ---------------------------------------------------------
# Web View Routes
# ---------------------------------------------------------

@auth_router.get("/login/", response_class=HTMLResponse, summary="Login Page (View Layer)")
def show_login_page(
    request: Request,
    error: Optional[str] = Query(None),
    next: Optional[str] = Query("/admin/")
):
    """Serves the UniBridge login web view"""
    # If already logged in as Admin, redirect directly to admin panel
    current_user = get_current_user_from_request(request)
    if current_user and current_user.role == "Admin" and not error:
        return RedirectResponse(url=next or "/admin/", status_code=303)

    return HTMLResponse(content=render_login_page(error=error, next_url=next or "/admin/"))


@auth_router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def show_login_page_no_slash(
    request: Request,
    error: Optional[str] = Query(None),
    next: Optional[str] = Query("/admin/")
):
    """Fallback without trailing slash"""
    return show_login_page(request, error=error, next=next)


@auth_router.post("/login/", summary="Form Login Endpoint", include_in_schema=False)
def form_login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    next: Optional[str] = Form("/admin/")
):
    """Processes web form login, sets session cookie, redirects to target URL"""
    user = authenticate_user(email.strip(), password.strip())
    if not user:
        return RedirectResponse(
            url=f"/login/?error=invalid_credentials&next={next or '/admin/'}",
            status_code=303
        )

    token = create_user_session(user.id)
    redirect_target = next if (next and next.startswith("/")) else "/admin/"
    res = RedirectResponse(url=redirect_target, status_code=303)
    res.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400 * 7,  # 7 days
        path="/"
    )
    return res


@auth_router.get("/logout/", summary="Logout Web Endpoint")
def web_logout(request: Request):
    """Clears session cookie and logs out current user"""
    token = request.cookies.get("session_token")
    if token:
        destroy_user_session(token)

    res = RedirectResponse(url="/login/?error=logged_out", status_code=303)
    res.delete_cookie(key="session_token", path="/")
    return res


@auth_router.get("/logout", include_in_schema=False)
def web_logout_no_slash(request: Request):
    return web_logout(request)


# ---------------------------------------------------------
# RESTful API Endpoints
# ---------------------------------------------------------

@auth_router.post(
    "/api/auth/login",
    summary="API Login Endpoint",
    description="Authenticates credentials and returns a Bearer session token + sets session_token cookie."
)
def api_login(payload: LoginRequest, response: Response):
    """Authenticates API requests and returns session token"""
    user = authenticate_user(payload.email.strip(), payload.password.strip())
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    token = create_user_session(user.id)
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=86400 * 7,
        path="/"
    )
    return {
        "message": "Login successful",
        "token": token,
        "token_type": "Bearer",
        "user": user
    }


@auth_router.post(
    "/api/auth/logout",
    summary="API Logout Endpoint",
    description="Terminates active session token."
)
def api_logout(request: Request, response: Response):
    """Terminates session via API"""
    token = request.cookies.get("session_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()

    if token:
        destroy_user_session(token)

    response.delete_cookie(key="session_token", path="/")
    return {"message": "Successfully logged out"}


@auth_router.get(
    "/api/auth/me",
    response_model=User,
    summary="Get Current Authenticated User",
    description="Returns profile of the currently logged-in user according to session token."
)
def api_get_me(request: Request):
    """Returns profile for currently authenticated user"""
    current_user = get_current_user_from_request(request)
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated. Provide session cookie or Authorization Bearer header."
        )
    return current_user
