"""
UserController - MVC Architecture
Controller dedicated to handling standard Web / Application User routes (/users).
Encapsulates CRUD functions for User operations.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from models.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPatch,
    UserModel
)

user_router = APIRouter(prefix="/users", tags=["Standard Users Controller"])


class UserController:
    """
    Standard User Controller Class.
    Implements core application CRUD logic for users.
    """

    # 1. READ ALL (GET /users)
    @staticmethod
    def list_users() -> List[User]:
        """CRUD: Retrieve all users"""
        return UserModel.get_all()

    # 2. READ BY ID (GET /users/{id})
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """CRUD: Retrieve a user by ID"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return user

    # 3. CREATE (POST /users)
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        """CRUD: Create a new user"""
        return UserModel.create(user_data)

    # 4. UPDATE (PUT /users/{id})
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """CRUD: Completely update user by ID"""
        updated_user = UserModel.update(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return updated_user

    # 5. PATCH (PATCH /users/{id})
    @staticmethod
    def patch_user(user_id: int, user_data: UserPatch) -> User:
        """CRUD: Partially update user by ID"""
        patched_user = UserModel.patch(user_id, user_data)
        if not patched_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return patched_user

    # 6. DELETE (DELETE /users/{id})
    @staticmethod
    def delete_user(user_id: int) -> dict:
        """CRUD: Remove user by ID"""
        deleted_user = UserModel.delete(user_id)
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return {
            "message": f"User with ID {user_id} deleted successfully",
            "deleted_user": deleted_user
        }


# ---------------------------------------------------------
# Connect Router Endpoints to UserController methods
# ---------------------------------------------------------

@user_router.get("", response_model=List[User], summary="List all users via UserController")
async def get_all_users():
    return UserController.list_users()


@user_router.get("/{id}", response_model=User, summary="Get user by ID via UserController")
async def get_single_user(id: int):
    return UserController.get_user_by_id(id)


@user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Create user via UserController")
async def create_new_user(user_data: UserCreate):
    return UserController.create_user(user_data)


@user_router.put("/{id}", response_model=User, summary="Full update user via UserController")
async def update_existing_user(id: int, user_data: UserUpdate):
    return UserController.update_user(id, user_data)


@user_router.patch("/{id}", response_model=User, summary="Partial update user via UserController")
async def patch_existing_user(id: int, user_data: UserPatch):
    return UserController.patch_user(id, user_data)


@user_router.delete("/{id}", summary="Delete user via UserController")
async def remove_user(id: int):
    return UserController.delete_user(id)
