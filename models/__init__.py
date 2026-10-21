"""
Models package for MVC architecture.
Contains User, Announcement, and JobPosting models, Pydantic schemas, and SQLAlchemy ORM entities.
"""
from models.user import (
    User,
    UserBase,
    UserCreate,
    UserUpdate,
    UserPatch,
    UserWithJobPostings,
    UserModel,
)
from models.announcement import (
    Announcement,
    AnnouncementBase,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementPatch,
    AnnouncementModel,
)
from models.job_posting import (
    JobPosting,
    JobPostingBase,
    JobPostingCreate,
    JobPostingUpdate,
    JobPostingPatch,
    JobPostingWithUser,
    JobPostingModel,
)
from models.db_entities import UserEntity, AnnouncementEntity, JobPostingEntity

__all__ = [
    # User Models
    "User",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPatch",
    "UserWithJobPostings",
    "UserModel",
    # Announcement Models
    "Announcement",
    "AnnouncementBase",
    "AnnouncementCreate",
    "AnnouncementUpdate",
    "AnnouncementPatch",
    "AnnouncementModel",
    # JobPosting Models
    "JobPosting",
    "JobPostingBase",
    "JobPostingCreate",
    "JobPostingUpdate",
    "JobPostingPatch",
    "JobPostingWithUser",
    "JobPostingModel",
    # ORM Entities
    "UserEntity",
    "AnnouncementEntity",
    "JobPostingEntity",
]
