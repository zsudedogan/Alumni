"""
JobPosting Model - MVC Architecture
Encapsulates JobPosting data structure, Pydantic schemas, and relational database CRUD operations using SQLAlchemy.
Derived from migration schema definitions and Data Design Document (ddd.md).
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from database import SessionLocal
from models.db_entities import JobPostingEntity, UserEntity


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class JobPostingBase(BaseModel):
    """Base schema with shared JobPosting attributes"""
    title: str = Field(..., min_length=1, max_length=120, description="Job title (Required, max 120 chars)")
    company: str = Field(..., min_length=1, description="Company name (Required)")
    city: Optional[str] = Field(None, description="Job city (Optional)")
    location: Optional[str] = Field("Remote", description="Job location (Optional, Default: Remote)")
    job_type: Optional[str] = "Full-time"
    description: Optional[str] = Field(None, description="Detailed job description (Optional)")
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[str] = None
    contact_email: Optional[str] = None
    user_id: Optional[int] = None


class JobPostingCreate(JobPostingBase):
    """Schema for creating a new job posting (POST /api/job-postings)"""
    pass


class JobPostingUpdate(JobPostingBase):
    """Schema for fully updating a job posting (PUT /api/job-postings/{id})"""
    pass


class JobPostingPatch(BaseModel):
    """Schema for partially updating a job posting (PATCH /api/job-postings/{id})"""
    title: Optional[str] = Field(None, min_length=1, max_length=120)
    company: Optional[str] = Field(None, min_length=1)
    city: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    salary_range: Optional[str] = None
    application_deadline: Optional[str] = None
    contact_email: Optional[str] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None


class JobPosting(JobPostingBase):
    """Full JobPosting entity model containing primary key and system fields"""
    id: int
    is_active: bool = True
    created_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class JobPostingWithUser(JobPosting):
    """JobPosting representation including the related user recruiter data"""
    user_name: Optional[str] = None
    user_email: Optional[str] = None


# ---------------------------------------------------------
# JobPosting Model Class (Database CRUD Repository)
# ---------------------------------------------------------
class JobPostingModel:
    """
    JobPosting Model repository interfacing with the database.
    Provides persistence and relationship querying with UserEntity.
    """

    # Baseline seed data for initial classroom setup
    _seed_data = [
        {
            "id": 1,
            "title": "Junior Python / FastAPI Developer",
            "company": "TechInnovate Istanbul",
            "location": "Istanbul / Hybrid",
            "job_type": "Full-time",
            "description": "Develop high-performance REST APIs using FastAPI, PostgreSQL, and Docker container architecture.",
            "requirements": "Python 3.11+, SQL/PostgreSQL, Git, RESTful API design principles.",
            "salary_range": "$1,800 - $2,500 / month",
            "application_deadline": "2026-11-30",
            "contact_email": "careers@techinnovate.com",
            "is_active": True,
            "created_at": "2026-10-21",
            "user_id": 1  # Associated with Emre Yilmaz
        },
        {
            "id": 2,
            "title": "Data Management & BI Intern",
            "company": "Global Analytics Corp",
            "location": "Remote",
            "job_type": "Internship",
            "description": "Assist the BI engineering team in ETL pipelines, schema design, and interactive dashboard reports.",
            "requirements": "Basic SQL, Python, Excel, interest in Management Information Systems.",
            "salary_range": "$800 - $1,100 / month",
            "application_deadline": "2026-12-15",
            "contact_email": "hr@globalanalytics.com",
            "is_active": True,
            "created_at": "2026-10-21",
            "user_id": 2  # Associated with Sude Dogan
        }
    ]

    @classmethod
    def _entity_to_pydantic(cls, entity: JobPostingEntity) -> JobPosting:
        """Converts an ORM entity to a Pydantic JobPosting schema"""
        city_val = getattr(entity, "city", None)
        loc_val = entity.location or city_val or "Remote"
        return JobPosting(
            id=entity.id,
            title=entity.title,
            company=entity.company,
            city=city_val or loc_val,
            location=loc_val,
            job_type=entity.job_type,
            description=entity.description,
            requirements=entity.requirements,
            salary_range=entity.salary_range,
            application_deadline=entity.application_deadline,
            contact_email=entity.contact_email,
            is_active=entity.is_active,
            created_at=entity.created_at,
            user_id=entity.user_id
        )

    @classmethod
    def _ensure_baseline_data(cls, db):
        """Ensures default classroom baseline postings exist if table is empty"""
        if db.query(JobPostingEntity).count() == 0:
            for item in cls._seed_data:
                posting = JobPostingEntity(**item)
                db.add(posting)
            db.commit()

    # 1. CREATE
    @classmethod
    def create(cls, data: JobPostingCreate) -> JobPosting:
        """CRUD: Create a new job posting in database"""
        payload = data.model_dump()
        if not payload.get("location") and payload.get("city"):
            payload["location"] = payload["city"]
        elif not payload.get("city") and payload.get("location"):
            payload["city"] = payload["location"]
        if not payload.get("created_at"):
            payload["created_at"] = datetime.now().strftime("%Y-%m-%d")
        if "is_active" not in payload or payload["is_active"] is None:
            payload["is_active"] = True

        db = SessionLocal()
        try:
            entity = JobPostingEntity(**payload)
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 2. READ ALL
    @classmethod
    def get_all(cls, active_only: bool = False, user_id: Optional[int] = None) -> List[JobPosting]:
        """CRUD: Read all job postings with optional filters"""
        db = SessionLocal()
        try:
            cls._ensure_baseline_data(db)
            query = db.query(JobPostingEntity)
            if active_only:
                query = query.filter(JobPostingEntity.is_active == True)
            if user_id is not None:
                query = query.filter(JobPostingEntity.user_id == user_id)

            entities = query.order_by(JobPostingEntity.id.asc()).all()
            return [cls._entity_to_pydantic(e) for e in entities]
        finally:
            db.close()

    # 3. READ BY ID
    @classmethod
    def get_by_id(cls, job_id: int) -> Optional[JobPosting]:
        """CRUD: Read a single job posting by ID"""
        db = SessionLocal()
        try:
            entity = db.query(JobPostingEntity).filter(JobPostingEntity.id == job_id).first()
            if entity:
                return cls._entity_to_pydantic(entity)
            return None
        finally:
            db.close()

    # 4. READ BY ID WITH RELATED USER (Demonstrating Relationship)
    @classmethod
    def get_with_user(cls, job_id: int) -> Optional[JobPostingWithUser]:
        """Retrieves a job posting along with the related User entity using relationship"""
        db = SessionLocal()
        try:
            entity = db.query(JobPostingEntity).filter(JobPostingEntity.id == job_id).first()
            if not entity:
                return None
            user_name = entity.user.name if entity.user else None
            user_email = entity.user.email if entity.user else None
            return JobPostingWithUser(
                id=entity.id,
                title=entity.title,
                company=entity.company,
                location=entity.location,
                job_type=entity.job_type,
                description=entity.description,
                requirements=entity.requirements,
                salary_range=entity.salary_range,
                application_deadline=entity.application_deadline,
                contact_email=entity.contact_email,
                is_active=entity.is_active,
                created_at=entity.created_at,
                user_id=entity.user_id,
                user_name=user_name,
                user_email=user_email
            )
        finally:
            db.close()

    # 5. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, job_id: int, data: JobPostingUpdate) -> Optional[JobPosting]:
        """CRUD: Full update of job posting attributes"""
        db = SessionLocal()
        try:
            entity = db.query(JobPostingEntity).filter(JobPostingEntity.id == job_id).first()
            if not entity:
                return None
            update_data = data.model_dump()
            entity.title = update_data["title"]
            entity.company = update_data["company"]
            entity.location = update_data.get("location", "Remote")
            entity.job_type = update_data.get("job_type", "Full-time")
            entity.description = update_data["description"]
            entity.requirements = update_data.get("requirements")
            entity.salary_range = update_data.get("salary_range")
            entity.application_deadline = update_data.get("application_deadline")
            entity.contact_email = update_data.get("contact_email")
            entity.user_id = update_data.get("user_id")
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 6. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, job_id: int, data: JobPostingPatch) -> Optional[JobPosting]:
        """CRUD: Partial update of job posting attributes"""
        db = SessionLocal()
        try:
            entity = db.query(JobPostingEntity).filter(JobPostingEntity.id == job_id).first()
            if not entity:
                return None
            patch_data = data.model_dump(exclude_unset=True)
            for field, value in patch_data.items():
                if hasattr(entity, field):
                    setattr(entity, field, value)
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 7. DELETE
    @classmethod
    def delete(cls, job_id: int) -> Optional[JobPosting]:
        """CRUD: Delete job posting by ID"""
        db = SessionLocal()
        try:
            entity = db.query(JobPostingEntity).filter(JobPostingEntity.id == job_id).first()
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
def create_job_posting_record(data: JobPostingCreate) -> JobPosting:
    return JobPostingModel.create(data)

def get_all_job_posting_records(active_only: bool = False) -> List[JobPosting]:
    return JobPostingModel.get_all(active_only=active_only)

def get_job_posting_record_by_id(job_id: int) -> Optional[JobPosting]:
    return JobPostingModel.get_by_id(job_id)

def update_job_posting_record(job_id: int, data: JobPostingUpdate) -> Optional[JobPosting]:
    return JobPostingModel.update(job_id, data)

def patch_job_posting_record(job_id: int, data: JobPostingPatch) -> Optional[JobPosting]:
    return JobPostingModel.patch(job_id, data)

def delete_job_posting_record(job_id: int) -> Optional[JobPosting]:
    return JobPostingModel.delete(job_id)
