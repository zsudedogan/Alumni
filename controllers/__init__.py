"""
Controllers package for MVC architecture.
Contains Controllers for Users, Announcements, and JobPostings (Direct & Nested routes).
"""
from controllers.user_controller import UserController, user_router
from controllers.api_user_controller import ApiUserController, api_user_router
from controllers.announcement_controller import AnnouncementController, announcement_router
from controllers.api_announcement_controller import ApiAnnouncementController, api_announcement_router
from controllers.job_posting_controller import JobPostingController, job_posting_router
from controllers.api_job_posting_controller import (
    ApiJobPostingController,
    api_job_posting_router,
    nested_job_posting_router,
)

__all__ = [
    # User Controllers
    "UserController",
    "user_router",
    "ApiUserController",
    "api_user_router",
    # Announcement Controllers
    "AnnouncementController",
    "announcement_router",
    "ApiAnnouncementController",
    "api_announcement_router",
    # Job Posting Controllers (Direct & Nested)
    "JobPostingController",
    "job_posting_router",
    "ApiJobPostingController",
    "api_job_posting_router",
    "nested_job_posting_router",
]
