"""
ApiUserController - MVC Architecture
Controller dedicated to handling REST API JSON requests for Users (/api/users).
Encapsulates CRUD functions for API operations.
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

api_user_router = APIRouter(prefix="/api/users", tags=["API Users Controller"])


class ApiUserController:
    """
    API User Controller Class.
    Implements CRUD operations for RESTful client requests.
    """

    # 1. READ ALL (GET /api/users)
    @staticmethod
    def list_users() -> List[User]:
        """CRUD: Read all users as JSON list"""
        return UserModel.get_all()

    # 2. READ BY ID (GET /api/users/{id})
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """CRUD: Read a single user by ID"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return user

    # 3. CREATE (POST /api/users)
    @staticmethod
    def create_user(user_data: UserCreate) -> User:
        """CRUD: Create a new user with status 201 Created"""
        return UserModel.create(user_data)

    # 4. UPDATE (PUT /api/users/{id})
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """CRUD: Full update of user attributes"""
        updated_user = UserModel.update(user_id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return updated_user

    # 5. PATCH (PATCH /api/users/{id})
    @staticmethod
    def patch_user(user_id: int, user_data: UserPatch) -> User:
        """CRUD: Partial update of user attributes"""
        patched_user = UserModel.patch(user_id, user_data)
        if not patched_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return patched_user

    # 6. DELETE (DELETE /api/users/{id})
    @staticmethod
    def delete_user(user_id: int) -> dict:
        """CRUD: Delete user by ID"""
        deleted_user = UserModel.delete(user_id)
        if not deleted_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return {
            "message": f"User with ID {user_id} has been successfully deleted",
            "deleted_user": deleted_user
        }


# ---------------------------------------------------------
# Connect Router Endpoints to ApiUserController methods
# ---------------------------------------------------------

@api_user_router.get("", response_model=List[User], summary="List all users via ApiUserController")
async def get_all_users():
    return ApiUserController.list_users()


@api_user_router.get("/{id}", response_model=User, summary="Get user by ID via ApiUserController")
async def get_single_user(id: int):
    return ApiUserController.get_user_by_id(id)


@api_user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Create user via ApiUserController")
async def create_new_user(user_data: UserCreate):
    return ApiUserController.create_user(user_data)


@api_user_router.put("/{id}", response_model=User, summary="Full update user via ApiUserController")
async def update_existing_user(id: int, user_data: UserUpdate):
    return ApiUserController.update_user(id, user_data)


@api_user_router.patch("/{id}", response_model=User, summary="Partial update user via ApiUserController")
async def patch_existing_user(id: int, user_data: UserPatch):
    return ApiUserController.patch_user(id, user_data)


@api_user_router.delete("/{id}", summary="Delete user via ApiUserController")
async def remove_user(id: int):
    return ApiUserController.delete_user(id)
