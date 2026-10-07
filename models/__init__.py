"""
Models package for MVC architecture.
Contains User and Announcement models.
"""
from models.user import User, UserBase, UserCreate, UserUpdate, UserPatch, UserModel
from models.announcement import (
    Announcement,
    AnnouncementBase,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementPatch,
    AnnouncementModel,
)

__all__ = [
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPatch",
    "UserModel",
    "Announcement",
    "AnnouncementBase",
    "AnnouncementCreate",
    "AnnouncementUpdate",
    "AnnouncementPatch",
    "AnnouncementModel",
]
