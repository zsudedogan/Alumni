"""
UserController - MVC Architecture
Controller dedicated to handling standard User routes (/users and /users/).
Encapsulates CRUD functions and exposes them via APIRouter.
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

USER_TAG = "UserController (/users)"

user_router = APIRouter(prefix="/users", tags=[USER_TAG])


class UserController:
    """
    Standard User Controller Class.
    Implements core application CRUD logic for users.
    """

    # 1. READ ALL (GET /users)
    @staticmethod
    def list_users() -> List[User]:
        """CRUD: Retrieve all users from UserModel"""
        return UserModel.get_all()

    # 2. READ BY ID (GET /users/{id})
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """CRUD: Retrieve a single user by ID from UserModel"""
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
        """CRUD: Create user via UserModel"""
        return UserModel.create(user_data)

    # 4. UPDATE (PUT /users/{id})
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """CRUD: Completely update user via UserModel"""
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
        """CRUD: Partially update user via UserModel"""
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
        """CRUD: Remove user via UserModel"""
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
# Routes: Map /users and /users/ to UserController
# ---------------------------------------------------------

# GET /users and /users/
@user_router.get("", response_model=List[User], summary="List all users [UserController]")
@user_router.get("/", response_model=List[User], include_in_schema=False)
async def get_all_users():
    """Retrieve all users via UserController"""
    return UserController.list_users()


# GET /users/{id}
@user_router.get("/{id}", response_model=User, summary="Get user by ID [UserController]")
async def get_single_user(id: int):
    """Retrieve a single user by ID via UserController"""
    return UserController.get_user_by_id(id)


# POST /users and /users/
@user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Create user [UserController]")
@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_user(user_data: UserCreate):
    """Create a new user via UserController"""
    return UserController.create_user(user_data)


# PUT /users/{id}
@user_router.put("/{id}", response_model=User, summary="Full update user (PUT) [UserController]")
async def update_existing_user(id: int, user_data: UserUpdate):
    """Fully replace an existing user via UserController"""
    return UserController.update_user(id, user_data)


# PATCH /users/{id}
@user_router.patch("/{id}", response_model=User, summary="Partial update user (PATCH) [UserController]")
async def patch_existing_user(id: int, user_data: UserPatch):
    """Partially update user attributes via UserController"""
    return UserController.patch_user(id, user_data)


# DELETE /users/{id}
@user_router.delete("/{id}", summary="Delete user [UserController]")
async def remove_user(id: int):
    """Delete a user by ID via UserController"""
    return UserController.delete_user(id)
