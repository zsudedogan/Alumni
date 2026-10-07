"""
User Model - MVC Architecture
Encapsulates User data structure and in-memory CRUD operations without any database connection.
"""

from typing import List, Optional
from pydantic import BaseModel


# ---------------------------------------------------------
# Pydantic Schemas / Entity Definitions
# ---------------------------------------------------------
class UserBase(BaseModel):
    """Base schema with common user attributes"""
    name: str
    age: Optional[int] = None
    email: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user (POST /api/users)"""
    pass


class UserUpdate(UserBase):
    """Schema for fully updating a user (PUT /api/users/{id})"""
    pass


class UserPatch(BaseModel):
    """Schema for partially updating a user (PATCH /api/users/{id})"""
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None


class User(UserBase):
    """User entity containing unique ID"""
    id: int


# ---------------------------------------------------------
# User Model Class (In-Memory CRUD without Database)
# ---------------------------------------------------------
class UserModel:
    """
    In-memory User Model repository.
    Handles data storage and CRUD operations without an external database.
    """
    # In-memory storage acting as temporary data store
    _users: List[User] = [
        User(id=1, name="Emre Yilmaz", age=24, email="emre@example.com"),
        User(id=2, name="Sude Dogan", age=22, email="sude@example.com"),
    ]
    _next_id: int = 3

    # 1. CREATE
    @classmethod
    def create(cls, user_data: UserCreate) -> User:
        """
        Creates a new user with an auto-incremented ID and saves to memory.
        CRUD: Create
        """
        new_user = User(id=cls._next_id, **user_data.model_dump())
        cls._next_id += 1
        cls._users.append(new_user)
        return new_user

    # 2. READ ALL
    @classmethod
    def get_all(cls) -> List[User]:
        """
        Retrieves all users from in-memory storage.
        CRUD: Read (List)
        """
        return cls._users

    # 3. READ BY ID
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[User]:
        """
        Finds and returns a single user by ID. Returns None if not found.
        CRUD: Read (Single)
        """
        for user in cls._users:
            if user.id == user_id:
                return user
        return None

    # 4. UPDATE (FULL - PUT)
    @classmethod
    def update(cls, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """
        Replaces all attributes of an existing user. Returns None if user not found.
        CRUD: Update (Full / PUT)
        """
        for index, user in enumerate(cls._users):
            if user.id == user_id:
                updated_user = User(id=user_id, **user_data.model_dump())
                cls._users[index] = updated_user
                return updated_user
        return None

    # 5. PATCH (PARTIAL - PATCH)
    @classmethod
    def patch(cls, user_id: int, user_data: UserPatch) -> Optional[User]:
        """
        Partially updates specified attributes of an existing user. Returns None if user not found.
        CRUD: Update (Partial / PATCH)
        """
        for index, user in enumerate(cls._users):
            if user.id == user_id:
                stored_dict = user.model_dump()
                update_dict = user_data.model_dump(exclude_unset=True)
                stored_dict.update(update_dict)
                patched_user = User(**stored_dict)
                cls._users[index] = patched_user
                return patched_user
        return None

    # 6. DELETE
    @classmethod
    def delete(cls, user_id: int) -> Optional[User]:
        """
        Removes a user with the specified ID from storage. Returns the deleted user or None.
        CRUD: Delete
        """
        for index, user in enumerate(cls._users):
            if user.id == user_id:
                return cls._users.pop(index)
        return None


# ---------------------------------------------------------
# Standalone Functional Helpers (For functional programming style)
# ---------------------------------------------------------
def create_user_record(user_data: UserCreate) -> User:
    return UserModel.create(user_data)

def get_all_user_records() -> List[User]:
    return UserModel.get_all()

def get_user_record_by_id(user_id: int) -> Optional[User]:
    return UserModel.get_by_id(user_id)

def update_user_record(user_id: int, user_data: UserUpdate) -> Optional[User]:
    return UserModel.update(user_id, user_data)

def patch_user_record(user_id: int, user_data: UserPatch) -> Optional[User]:
    return UserModel.patch(user_id, user_data)

def delete_user_record(user_id: int) -> Optional[User]:
    return UserModel.delete(user_id)
