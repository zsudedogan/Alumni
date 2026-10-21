"""
Views package for MVC architecture.
Contains View Layer rendering HTML management interfaces and presentation templates.
"""
from views.user_view import render_user_management_page
from views.announcement_view import render_announcement_management_page
from views.job_posting_view import render_job_posting_management_page

__all__ = [
    "render_user_management_page",
    "render_announcement_management_page",
    "render_job_posting_management_page",
]
