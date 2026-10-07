"""
Controllers package for MVC architecture.
Contains Controllers for Users and Announcements.
"""
from controllers.user_controller import UserController, user_router
from controllers.api_user_controller import ApiUserController, api_user_router
from controllers.announcement_controller import AnnouncementController, announcement_router
from controllers.api_announcement_controller import ApiAnnouncementController, api_announcement_router

__all__ = [
    "UserController",
    "user_router",
    "ApiUserController",
    "api_user_router",
    "AnnouncementController",
    "announcement_router",
    "ApiAnnouncementController",
    "api_announcement_router",
]
