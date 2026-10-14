"""
Announcement Model - MVC Architecture
Encapsulates Announcement data structure and relational database CRUD operations using SQLAlchemy.
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from database import SessionLocal
from models.db_entities import AnnouncementEntity


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class AnnouncementBase(BaseModel):
    """Base schema for Announcement entity"""
    title: str
    content: str
    author: Optional[str] = "Admin"
    category: Optional[str] = "General"
    date: Optional[str] = None


class AnnouncementCreate(AnnouncementBase):
    """Schema for creating a new announcement"""
    pass


class AnnouncementUpdate(AnnouncementBase):
    """Schema for fully updating an announcement"""
    pass


class AnnouncementPatch(BaseModel):
    """Schema for partially updating an announcement"""
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None


class Announcement(AnnouncementBase):
    """Full Announcement entity with unique ID"""
    id: int


# ---------------------------------------------------------
# Announcement Model Class (Database CRUD Repository)
# ---------------------------------------------------------
class AnnouncementModel:
    """
    Announcement Model repository interfacing with the database.
    Provides persistence across restarts and container lifecycle.
    """

    # Baseline seed data
    _seed_data = [
        {
            "id": 1,
            "title": "Welcome to Week 04 MVC Architecture",
            "content": "We have successfully modularized our API into Model, View, and Controller layers.",
            "author": "Department of Management Information Systems",
            "category": "Academic",
            "date": "2026-10-07"
        },
        {
            "id": 2,
            "title": "Midterm Project Submissions",
            "content": "Please ensure your repository has updated README documentation and all CRUD routes working.",
            "author": "Course Instructor",
            "category": "Urgent",
            "date": "2026-10-08"
        }
    ]

    @classmethod
    def _ensure_baseline_data(cls, db):
        """Ensures default classroom baseline records exist if table is empty"""
        if db.query(AnnouncementEntity).count() == 0:
            for item in cls._seed_data:
                ann = AnnouncementEntity(
                    id=item["id"],
                    title=item["title"],
                    content=item["content"],
                    author=item["author"],
                    category=item["category"],
                    date=item["date"]
                )
                db.add(ann)
            db.commit()

    # 1. CREATE
    @classmethod
    def create(cls, data: AnnouncementCreate) -> Announcement:
        """CRUD: Create announcement in database"""
        ann_dict = data.model_dump()
        if not ann_dict.get("date"):
            ann_dict["date"] = datetime.now().strftime("%Y-%m-%d")

        db = SessionLocal()
        try:
            entity = AnnouncementEntity(**ann_dict)
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return Announcement(
                id=entity.id,
                title=entity.title,
                content=entity.content,
                author=entity.author,
                category=entity.category,
                date=entity.date
            )
        finally:
            db.close()

    # 2. READ ALL
    @classmethod
    def get_all(cls) -> List[Announcement]:
        """CRUD: Read all announcements from database"""
        db = SessionLocal()
        try:
            cls._ensure_baseline_data(db)
            entities = db.query(AnnouncementEntity).order_by(AnnouncementEntity.id.asc()).all()
            return [
                Announcement(
                    id=e.id,
                    title=e.title,
                    content=e.content,
                    author=e.author,
                    category=e.category,
                    date=e.date
                )
                for e in entities
            ]
        finally:
            db.close()

    # 3. READ BY ID
    @classmethod
    def get_by_id(cls, ann_id: int) -> Optional[Announcement]:
        """CRUD: Read a single announcement by ID"""
        db = SessionLocal()
        try:
            e = db.query(AnnouncementEntity).filter(AnnouncementEntity.id == ann_id).first()
            if e:
                return Announcement(
                    id=e.id,
                    title=e.title,
                    content=e.content,
                    author=e.author,
                    category=e.category,
                    date=e.date
                )
            return None
        finally:
            db.close()

    # 4. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, ann_id: int, data: AnnouncementUpdate) -> Optional[Announcement]:
        """CRUD: Full update of announcement attributes in database"""
        db = SessionLocal()
        try:
            e = db.query(AnnouncementEntity).filter(AnnouncementEntity.id == ann_id).first()
            if not e:
                return None
            ann_dict = data.model_dump()
            e.title = ann_dict["title"]
            e.content = ann_dict["content"]
            e.author = ann_dict.get("author", "Admin")
            e.category = ann_dict.get("category", "General")
            if ann_dict.get("date"):
                e.date = ann_dict["date"]
            db.commit()
            db.refresh(e)
            return Announcement(
                id=e.id,
                title=e.title,
                content=e.content,
                author=e.author,
                category=e.category,
                date=e.date
            )
        finally:
            db.close()

    # 5. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, ann_id: int, data: AnnouncementPatch) -> Optional[Announcement]:
        """CRUD: Partial update of announcement attributes in database"""
        db = SessionLocal()
        try:
            e = db.query(AnnouncementEntity).filter(AnnouncementEntity.id == ann_id).first()
            if not e:
                return None
            patch_dict = data.model_dump(exclude_unset=True)
            if "title" in patch_dict and patch_dict["title"] is not None:
                e.title = patch_dict["title"]
            if "content" in patch_dict and patch_dict["content"] is not None:
                e.content = patch_dict["content"]
            if "author" in patch_dict and patch_dict["author"] is not None:
                e.author = patch_dict["author"]
            if "category" in patch_dict and patch_dict["category"] is not None:
                e.category = patch_dict["category"]
            if "date" in patch_dict and patch_dict["date"] is not None:
                e.date = patch_dict["date"]
            db.commit()
            db.refresh(e)
            return Announcement(
                id=e.id,
                title=e.title,
                content=e.content,
                author=e.author,
                category=e.category,
                date=e.date
            )
        finally:
            db.close()

    # 6. DELETE
    @classmethod
    def delete(cls, ann_id: int) -> Optional[Announcement]:
        """CRUD: Delete announcement by ID from database"""
        db = SessionLocal()
        try:
            e = db.query(AnnouncementEntity).filter(AnnouncementEntity.id == ann_id).first()
            if not e:
                return None
            deleted = Announcement(
                id=e.id,
                title=e.title,
                content=e.content,
                author=e.author,
                category=e.category,
                date=e.date
            )
            db.delete(e)
            db.commit()
            return deleted
        finally:
            db.close()


# ---------------------------------------------------------
# Standalone Functional Helpers
# ---------------------------------------------------------
def create_announcement_record(data: AnnouncementCreate) -> Announcement:
    return AnnouncementModel.create(data)

def get_all_announcement_records() -> List[Announcement]:
    return AnnouncementModel.get_all()

def get_announcement_record_by_id(ann_id: int) -> Optional[Announcement]:
    return AnnouncementModel.get_by_id(ann_id)

def update_announcement_record(ann_id: int, data: AnnouncementUpdate) -> Optional[Announcement]:
    return AnnouncementModel.update(ann_id, data)

def patch_announcement_record(ann_id: int, data: AnnouncementPatch) -> Optional[Announcement]:
    return AnnouncementModel.patch(ann_id, data)

def delete_announcement_record(ann_id: int) -> Optional[Announcement]:
    return AnnouncementModel.delete(ann_id)
