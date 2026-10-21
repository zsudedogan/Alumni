"""
Models package for MVC architecture.
Contains User and Announcement models, Pydantic schemas, and SQLAlchemy ORM entities.
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
from models.db_entities import UserEntity, AnnouncementEntity, JobPostingEntity

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
    "UserEntity",
    "AnnouncementEntity",
    "JobPostingEntity",
]

