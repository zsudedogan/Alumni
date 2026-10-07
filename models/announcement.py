"""
Announcement Model - MVC Architecture
Encapsulates Announcement entity schemas and in-memory CRUD operations without any database connection.
Homework Requirement: 'Create Announcement model without database yet'.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class AnnouncementBase(BaseModel):
    """Base schema for Announcement fields"""
    title: str
    content: str
    author: Optional[str] = "Admin"
    category: Optional[str] = "General"
    date: Optional[str] = None


class AnnouncementCreate(AnnouncementBase):
    """Schema for creating a new announcement"""
    pass


class AnnouncementUpdate(AnnouncementBase):
    """Schema for fully updating an announcement (PUT)"""
    pass


class AnnouncementPatch(BaseModel):
    """Schema for partially updating an announcement (PATCH)"""
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None


class Announcement(AnnouncementBase):
    """Announcement entity with assigned ID"""
    id: int


# ---------------------------------------------------------
# Announcement Model Class (In-Memory CRUD without Database)
# ---------------------------------------------------------
class AnnouncementModel:
    """
    In-memory Announcement Model repository.
    Handles data storage and CRUD operations without an external database.
    """
    _announcements: List[Announcement] = [
        Announcement(
            id=1,
            title="Welcome to Week 04 MVC Architecture",
            content="We have successfully modularized our API into Model, View, and Controller layers.",
            author="Department of Management Information Systems",
            category="Academic",
            date="2026-10-07"
        ),
        Announcement(
            id=2,
            title="Midterm Project Submissions",
            content="Please ensure your repository has updated README documentation and all CRUD routes working.",
            author="Course Instructor",
            category="Urgent",
            date="2026-10-08"
        )
    ]
    _next_id: int = 3

    # 1. CREATE
    @classmethod
    def create(cls, data: AnnouncementCreate) -> Announcement:
        """CRUD: Create announcement with auto-increment ID"""
        ann_dict = data.model_dump()
        if not ann_dict.get("date"):
            ann_dict["date"] = datetime.now().strftime("%Y-%m-%d")

        new_ann = Announcement(id=cls._next_id, **ann_dict)
        cls._next_id += 1
        cls._announcements.append(new_ann)
        return new_ann

    # 2. READ ALL
    @classmethod
    def get_all(cls) -> List[Announcement]:
        """CRUD: Read all announcements"""
        return cls._announcements

    # 3. READ BY ID
    @classmethod
    def get_by_id(cls, ann_id: int) -> Optional[Announcement]:
        """CRUD: Read a single announcement by ID"""
        for ann in cls._announcements:
            if ann.id == ann_id:
                return ann
        return None

    # 4. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, ann_id: int, data: AnnouncementUpdate) -> Optional[Announcement]:
        """CRUD: Full update of announcement attributes"""
        for index, ann in enumerate(cls._announcements):
            if ann.id == ann_id:
                ann_dict = data.model_dump()
                if not ann_dict.get("date"):
                    ann_dict["date"] = ann.date
                updated = Announcement(id=ann_id, **ann_dict)
                cls._announcements[index] = updated
                return updated
        return None

    # 5. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, ann_id: int, data: AnnouncementPatch) -> Optional[Announcement]:
        """CRUD: Partial update of announcement attributes"""
        for index, ann in enumerate(cls._announcements):
            if ann.id == ann_id:
                stored_dict = ann.model_dump()
                update_dict = data.model_dump(exclude_unset=True)
                stored_dict.update(update_dict)
                patched = Announcement(**stored_dict)
                cls._announcements[index] = patched
                return patched
        return None

    # 6. DELETE
    @classmethod
    def delete(cls, ann_id: int) -> Optional[Announcement]:
        """CRUD: Delete announcement by ID"""
        for index, ann in enumerate(cls._announcements):
            if ann.id == ann_id:
                return cls._announcements.pop(index)
        return None
