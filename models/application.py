"""
Application Model - MVC Architecture
Encapsulates Application data structure, Pydantic schemas, and relational database CRUD operations using SQLAlchemy.
Derived from migration schema definitions and Data Design Document (ddd.md).
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict
from database import SessionLocal
from models.db_entities import ApplicationEntity, JobPostingEntity, UserEntity


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class ApplicationBase(BaseModel):
    """Base schema with shared Application attributes"""
    job_id: int
    user_id: int
    resume_url: Optional[str] = None
    cover_note: Optional[str] = None
    status: Optional[str] = "Pending"


class ApplicationCreate(BaseModel):
    """Schema for creating a new job application (POST /api/applications)"""
    job_id: Optional[int] = None
    user_id: Optional[int] = None
    resume_url: Optional[str] = None
    cover_note: Optional[str] = None
    status: Optional[str] = "Pending"


class ApplicationUpdate(ApplicationBase):
    """Schema for fully updating an application (PUT /api/applications/{id})"""
    pass


class ApplicationPatch(BaseModel):
    """Schema for partially updating an application (PATCH /api/applications/{id})"""
    job_id: Optional[int] = None
    user_id: Optional[int] = None
    resume_url: Optional[str] = None
    cover_note: Optional[str] = None
    status: Optional[str] = None


class Application(ApplicationBase):
    """Full Application entity model containing primary key and system fields"""
    id: int
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ApplicationWithDetails(Application):
    """Application representation including related applicant user and job posting details"""
    applicant_name: Optional[str] = None
    applicant_email: Optional[str] = None
    job_title: Optional[str] = None
    company: Optional[str] = None


# ---------------------------------------------------------
# Application Model Class (Database CRUD Repository)
# ---------------------------------------------------------
class ApplicationModel:
    """
    Application Model repository interfacing with the database.
    Provides persistence and relationship querying with UserEntity and JobPostingEntity.
    """

    # Baseline seed data for initial classroom setup
    _seed_data = [
        {
            "id": 1,
            "job_id": 1,
            "user_id": 2,  # Sude Dogan applying to TechInnovate
            "resume_url": "https://linkedin.com/in/sudedogan",
            "cover_note": "Experienced with Python, FastAPI, and database migrations. Highly motivated for this position.",
            "status": "Pending",
            "created_at": "2026-10-21"
        }
    ]

    @classmethod
    def _entity_to_pydantic(cls, entity: ApplicationEntity) -> Application:
        """Converts an ORM entity to a Pydantic Application schema"""
        return Application(
            id=entity.id,
            job_id=entity.job_id,
            user_id=entity.user_id,
            resume_url=entity.resume_url,
            cover_note=entity.cover_note,
            status=entity.status,
            created_at=entity.created_at
        )

    @classmethod
    def _entity_to_details_pydantic(cls, entity: ApplicationEntity) -> ApplicationWithDetails:
        """Converts an ORM entity to an enriched ApplicationWithDetails schema"""
        applicant_name = entity.user.name if entity.user else None
        applicant_email = entity.user.email if entity.user else None
        job_title = entity.job_posting.title if entity.job_posting else None
        company = entity.job_posting.company if entity.job_posting else None

        return ApplicationWithDetails(
            id=entity.id,
            job_id=entity.job_id,
            user_id=entity.user_id,
            resume_url=entity.resume_url,
            cover_note=entity.cover_note,
            status=entity.status,
            created_at=entity.created_at,
            applicant_name=applicant_name,
            applicant_email=applicant_email,
            job_title=job_title,
            company=company
        )

    @classmethod
    def _ensure_baseline_data(cls, db):
        """Ensures default classroom baseline application exists if table is empty and parent records exist"""
        if db.query(ApplicationEntity).count() == 0:
            # Check if referenced job and user exist
            job = db.query(JobPostingEntity).filter(JobPostingEntity.id == 1).first()
            user = db.query(UserEntity).filter(UserEntity.id == 2).first()
            if job and user:
                for item in cls._seed_data:
                    app_record = ApplicationEntity(**item)
                    db.add(app_record)
                db.commit()

    # 1. CREATE
    @classmethod
    def create(cls, data: ApplicationCreate) -> Application:
        """CRUD: Create a new application in database"""
        payload = data.model_dump()
        if not payload.get("created_at"):
            payload["created_at"] = datetime.now().strftime("%Y-%m-%d")
        if not payload.get("status"):
            payload["status"] = "Pending"

        db = SessionLocal()
        try:
            entity = ApplicationEntity(**payload)
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 2. READ ALL
    @classmethod
    def get_all(
        cls,
        job_id: Optional[int] = None,
        user_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> List[Application]:
        """CRUD: Read all applications with optional filtering"""
        db = SessionLocal()
        try:
            cls._ensure_baseline_data(db)
            query = db.query(ApplicationEntity)
            if job_id is not None:
                query = query.filter(ApplicationEntity.job_id == job_id)
            if user_id is not None:
                query = query.filter(ApplicationEntity.user_id == user_id)
            if status is not None:
                query = query.filter(ApplicationEntity.status == status)

            entities = query.order_by(ApplicationEntity.id.asc()).all()
            return [cls._entity_to_pydantic(e) for e in entities]
        finally:
            db.close()

    # 3. READ ALL WITH DETAILS
    @classmethod
    def get_all_with_details(
        cls,
        job_id: Optional[int] = None,
        user_id: Optional[int] = None
    ) -> List[ApplicationWithDetails]:
        """CRUD: Read all applications resolving User and JobPosting details"""
        db = SessionLocal()
        try:
            cls._ensure_baseline_data(db)
            query = db.query(ApplicationEntity)
            if job_id is not None:
                query = query.filter(ApplicationEntity.job_id == job_id)
            if user_id is not None:
                query = query.filter(ApplicationEntity.user_id == user_id)

            entities = query.order_by(ApplicationEntity.id.asc()).all()
            return [cls._entity_to_details_pydantic(e) for e in entities]
        finally:
            db.close()

    # 4. READ BY ID
    @classmethod
    def get_by_id(cls, app_id: int) -> Optional[Application]:
        """CRUD: Read a single application by ID"""
        db = SessionLocal()
        try:
            entity = db.query(ApplicationEntity).filter(ApplicationEntity.id == app_id).first()
            if entity:
                return cls._entity_to_pydantic(entity)
            return None
        finally:
            db.close()

    # 5. READ BY ID WITH DETAILS
    @classmethod
    def get_with_details(cls, app_id: int) -> Optional[ApplicationWithDetails]:
        """Retrieves an application along with applicant user and job posting details"""
        db = SessionLocal()
        try:
            entity = db.query(ApplicationEntity).filter(ApplicationEntity.id == app_id).first()
            if not entity:
                return None
            return cls._entity_to_details_pydantic(entity)
        finally:
            db.close()

    # 6. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, app_id: int, data: ApplicationUpdate) -> Optional[Application]:
        """CRUD: Full update of application attributes"""
        db = SessionLocal()
        try:
            entity = db.query(ApplicationEntity).filter(ApplicationEntity.id == app_id).first()
            if not entity:
                return None
            update_data = data.model_dump()
            entity.job_id = update_data["job_id"]
            entity.user_id = update_data["user_id"]
            entity.resume_url = update_data.get("resume_url")
            entity.cover_note = update_data.get("cover_note")
            entity.status = update_data.get("status", "Pending")
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 7. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, app_id: int, data: ApplicationPatch) -> Optional[Application]:
        """CRUD: Partial update of application attributes"""
        db = SessionLocal()
        try:
            entity = db.query(ApplicationEntity).filter(ApplicationEntity.id == app_id).first()
            if not entity:
                return None
            patch_data = data.model_dump(exclude_unset=True)
            for field, value in patch_data.items():
                if hasattr(entity, field) and value is not None:
                    setattr(entity, field, value)
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 8. DELETE
    @classmethod
    def delete(cls, app_id: int) -> Optional[Application]:
        """CRUD: Delete application by ID"""
        db = SessionLocal()
        try:
            entity = db.query(ApplicationEntity).filter(ApplicationEntity.id == app_id).first()
            if not entity:
                return None
            deleted = cls._entity_to_pydantic(entity)
            db.delete(entity)
            db.commit()
            return deleted
        finally:
            db.close()


# ---------------------------------------------------------
# Standalone Functional Helpers
# ---------------------------------------------------------
def create_application_record(data: ApplicationCreate) -> Application:
    return ApplicationModel.create(data)

def get_all_application_records(job_id: Optional[int] = None, user_id: Optional[int] = None) -> List[Application]:
    return ApplicationModel.get_all(job_id=job_id, user_id=user_id)

def get_application_record_by_id(app_id: int) -> Optional[Application]:
    return ApplicationModel.get_by_id(app_id)

def update_application_record(app_id: int, data: ApplicationUpdate) -> Optional[Application]:
    return ApplicationModel.update(app_id, data)

def patch_application_record(app_id: int, data: ApplicationPatch) -> Optional[Application]:
    return ApplicationModel.patch(app_id, data)

def delete_application_record(app_id: int) -> Optional[Application]:
    return ApplicationModel.delete(app_id)
