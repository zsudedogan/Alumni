"""
Register Controller - MVC Architecture
Handles User Registration HTTP requests (Web View and API Auth endpoints).
"""

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from models.user import (
    User,
    UserRegister,
    register_user_record,
    get_user_record_by_email,
)
from views.register_view import render_register_page

register_router = APIRouter(tags=["Authentication & Registration"])


class RegisterController:
    """
    Controller handling user registration workflow.
    Provides web interface and RESTful JSON endpoint for account creation.
    """

    ALLOWED_ROLES = {"Student", "Alumni", "Recruiter", "Academic"}

    @classmethod
    def get_register_page(cls) -> HTMLResponse:
        """Renders the HTML registration view"""
        return HTMLResponse(content=render_register_page())

    @classmethod
    def register_user(cls, user_data: UserRegister) -> User:
        """
        Validates and registers a new user with chosen role and profile details.
        """
        # Validate role
        if user_data.role not in cls.ALLOWED_ROLES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role '{user_data.role}'. Allowed roles: {', '.join(cls.ALLOWED_ROLES)}"
            )

        # Validate password strength
        if len(user_data.password.strip()) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long."
            )

        # Check unique email
        existing_user = get_user_record_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with email '{user_data.email}' already exists. Please log in or use a different email."
            )

        created_user = register_user_record(user_data)
        return created_user


# ---------------------------------------------------------
# Route Handlers
# ---------------------------------------------------------

@register_router.get("/register/", response_class=HTMLResponse, summary="Registration Page (View Layer)")
def show_register_page():
    """Serves the user registration web view"""
    return RegisterController.get_register_page()


@register_router.get("/register", response_class=HTMLResponse, include_in_schema=False)
def show_register_page_no_slash():
    """Fallback redirect / alias without trailing slash"""
    return RegisterController.get_register_page()


@register_router.post(
    "/api/auth/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User with Role",
    description="Registers a new user into the ecosystem with role (Student, Alumni, Recruiter, Academic), department, bio, and credentials."
)
def api_register_user(payload: UserRegister):
    """API endpoint to create a registered user account"""
    return RegisterController.register_user(payload)


@register_router.post(
    "/register/",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Form Registration Endpoint",
    include_in_schema=False
)
def form_register_user(payload: UserRegister):
    """Fallback endpoint for form submissions"""
    return RegisterController.register_user(payload)
