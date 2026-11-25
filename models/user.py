"""
User Model - MVC Architecture
Encapsulates User data structure and relational database CRUD operations using SQLAlchemy.
"""

from typing import List, Optional, Union
from datetime import datetime
from pydantic import BaseModel
from database import SessionLocal
from models.db_entities import UserEntity


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class UserBase(BaseModel):
    """Base schema with common user attributes"""
    name: str
    age: Optional[int] = None
    email: Optional[str] = None
    role: str = "Student"
    department: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user (POST /api/users)"""
    password: Optional[str] = None


class UserRegister(BaseModel):
    """Schema for registering a new user (POST /register/ or POST /api/auth/register)"""
    name: str
    email: str
    password: str
    role: str = "Student"
    department: Optional[str] = None
    age: Optional[int] = None
    bio: Optional[str] = None


class UserUpdate(UserBase):
    """Schema for fully updating a user (PUT /api/users/{id})"""
    password: Optional[str] = None


class UserPatch(BaseModel):
    """Schema for partially updating a user (PATCH /api/users/{id})"""
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    """User entity containing unique ID and audit metadata (public representation, excludes password)"""
    id: int
    created_at: Optional[str] = None


class UserWithJobPostings(User):
    """User entity including list of posted job openings (demonstrating 1-to-many relationship)"""
    job_postings: List[dict] = []



# ---------------------------------------------------------
# User Model Class (Database CRUD Repository)
# ---------------------------------------------------------
class UserModel:
    """
    User Model repository interfacing with the database.
    Provides persistence across restarts and container lifecycle.
    """

    # Baseline seed data for initial setup
    _seed_data = [
        {"id": 1, "name": "Emre Yilmaz", "age": 24, "email": "emre@example.com", "role": "Alumni", "department": "Computer Engineering", "password": "password123"},
        {"id": 2, "name": "Sude Dogan", "age": 22, "email": "sude@example.com", "role": "Admin", "department": "Management Information Systems", "password": "password123"},
    ]

    @staticmethod
    def _entity_to_pydantic(entity: UserEntity) -> User:
        """Converts SQLAlchemy UserEntity to public Pydantic User schema"""
        return User(
            id=entity.id,
            name=entity.name,
            age=entity.age,
            email=entity.email,
            role=entity.role or "Student",
            department=entity.department,
            bio=entity.bio,
            created_at=entity.created_at,
        )

    @classmethod
    def _ensure_baseline_data(cls, db):
        """Ensures default classroom baseline records exist if table is empty"""
        if db.query(UserEntity).count() == 0:
            for item in cls._seed_data:
                user = UserEntity(
                    id=item["id"],
                    name=item["name"],
                    age=item["age"],
                    email=item["email"],
                    role=item.get("role", "Student"),
                    department=item.get("department"),
                    password=item.get("password"),
                    created_at="2026-11-01 10:00"
                )
                db.add(user)
            db.commit()

    # 1. CREATE
    @classmethod
    def create(cls, user_data: Union[UserCreate, UserRegister]) -> User:
        """
        Creates a new user in the database with auto-increment ID.
        CRUD: Create
        """
        db = SessionLocal()
        try:
            dump = user_data.model_dump()
            if not dump.get("created_at"):
                dump["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            if not dump.get("role"):
                dump["role"] = "Student"
            entity = UserEntity(**dump)
            db.add(entity)
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 2. READ ALL
    @classmethod
    def get_all(cls) -> List[User]:
        """
        Retrieves all users from the database ordered by ID.
        CRUD: Read (List)
        """
        db = SessionLocal()
        try:
            cls._ensure_baseline_data(db)
            entities = db.query(UserEntity).order_by(UserEntity.id.asc()).all()
            return [cls._entity_to_pydantic(e) for e in entities]
        finally:
            db.close()

    # 3. READ BY ID
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[User]:
        """
        Finds and returns a single user by ID. Returns None if not found.
        CRUD: Read (Single)
        """
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if entity:
                return cls._entity_to_pydantic(entity)
            return None
        finally:
            db.close()

    # 3b. READ BY EMAIL
    @classmethod
    def get_by_email(cls, email: str) -> Optional[User]:
        """
        Finds and returns a single user by email. Returns None if not found.
        """
        if not email:
            return None
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.email == email).first()
            if entity:
                return cls._entity_to_pydantic(entity)
            return None
        finally:
            db.close()

    # 3c. AUTHENTICATE
    @classmethod
    def authenticate(cls, email: str, password: str) -> Optional[User]:
        """
        Validates user credentials against database. Returns User if valid, None otherwise.
        """
        if not email:
            return None
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.email == email.strip().lower()).first()
            if not entity:
                # Try exact match if case-sensitive
                entity = db.query(UserEntity).filter(UserEntity.email == email.strip()).first()
            if not entity:
                return None
            # Check password
            if entity.password and entity.password == password.strip():
                return cls._entity_to_pydantic(entity)
            return None
        finally:
            db.close()

    # 4. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Replaces all attributes of an existing user in the database. Returns None if user not found.
        CRUD: Update (Full / PUT)
        """
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not entity:
                return None
            data = user_data.model_dump()
            entity.name = data["name"]
            entity.age = data.get("age")
            entity.email = data.get("email")
            if "role" in data and data["role"] is not None:
                entity.role = data["role"]
            if "department" in data:
                entity.department = data["department"]
            if "bio" in data:
                entity.bio = data["bio"]
            if "password" in data and data["password"]:
                entity.password = data["password"]
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 5. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, user_id: int, user_data: UserPatch) -> Optional[User]:
        """
        Partially updates specified attributes of an existing user. Returns None if user not found.
        CRUD: Update (Partial / PATCH)
        """
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not entity:
                return None
            data = user_data.model_dump(exclude_unset=True)
            if "name" in data and data["name"] is not None:
                entity.name = data["name"]
            if "age" in data:
                entity.age = data["age"]
            if "email" in data:
                entity.email = data["email"]
            if "role" in data and data["role"] is not None:
                entity.role = data["role"]
            if "department" in data:
                entity.department = data["department"]
            if "bio" in data:
                entity.bio = data["bio"]
            if "password" in data and data["password"] is not None:
                entity.password = data["password"]
            db.commit()
            db.refresh(entity)
            return cls._entity_to_pydantic(entity)
        finally:
            db.close()

    # 6. DELETE
    @classmethod
    def delete(cls, user_id: int) -> Optional[User]:
        """
        Removes a user with the specified ID from the database. Returns the deleted user or None.
        CRUD: Delete
        """
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not entity:
                return None
            deleted_user = cls._entity_to_pydantic(entity)
            db.delete(entity)
            db.commit()
            return deleted_user
        finally:
            db.close()

    # 7. READ USER WITH JOB POSTINGS (Demonstrating Relationship)
    @classmethod
    def get_user_with_jobs(cls, user_id: int) -> Optional[UserWithJobPostings]:
        """Fetches a user along with all job postings they created using the ORM relationship"""
        db = SessionLocal()
        try:
            entity = db.query(UserEntity).filter(UserEntity.id == user_id).first()
            if not entity:
                return None
            jobs_summary = [
                {
                    "id": j.id,
                    "title": j.title,
                    "company": j.company,
                    "location": j.location,
                    "job_type": j.job_type,
                    "is_active": j.is_active
                }
                for j in entity.job_postings
            ]
            return UserWithJobPostings(
                id=entity.id,
                name=entity.name,
                age=entity.age,
                email=entity.email,
                role=entity.role or "Student",
                department=entity.department,
                bio=entity.bio,
                created_at=entity.created_at,
                job_postings=jobs_summary
            )
        finally:
            db.close()



# ---------------------------------------------------------
# Standalone Functional Helpers
# ---------------------------------------------------------
def create_user_record(user_data: UserCreate) -> User:
    return UserModel.create(user_data)

def register_user_record(user_data: UserRegister) -> User:
    return UserModel.create(user_data)

def get_all_user_records() -> List[User]:
    return UserModel.get_all()

def get_user_record_by_id(user_id: int) -> Optional[User]:
    return UserModel.get_by_id(user_id)

def get_user_record_by_email(email: str) -> Optional[User]:
    return UserModel.get_by_email(email)

def update_user_record(user_id: int, user_data: UserUpdate) -> Optional[User]:
    return UserModel.update(user_id, user_data)

def patch_user_record(user_id: int, user_data: UserPatch) -> Optional[User]:
    return UserModel.patch(user_id, user_data)

def delete_user_record(user_id: int) -> Optional[User]:
    return UserModel.delete(user_id)

def authenticate_user(email: str, password: str) -> Optional[User]:
    return UserModel.authenticate(email, password)

