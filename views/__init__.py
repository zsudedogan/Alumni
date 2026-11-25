"""
Views package for MVC architecture.
Contains View Layer rendering HTML management interfaces and presentation templates.
"""
from views.user_view import render_user_management_page
from views.announcement_view import render_announcement_management_page
from views.job_posting_view import render_job_posting_management_page
from views.application_view import render_application_management_page
from views.login_view import render_login_page
from views.admin_view import render_admin_dashboard
from views.portal_views import (
    render_student_portal,
    render_alumni_portal,
    render_recruiter_portal,
    render_academic_portal,
)

__all__ = [
    "render_user_management_page",
    "render_announcement_management_page",
    "render_job_posting_management_page",
    "render_application_management_page",
    "render_login_page",
    "render_admin_dashboard",
    "render_student_portal",
    "render_alumni_portal",
    "render_recruiter_portal",
    "render_academic_portal",
]


