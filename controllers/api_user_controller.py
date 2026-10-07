"""
ApiUserController - MVC Architecture
Controller dedicated to handling REST API requests for Users (/api/users and /api/users/).
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

API_TAG = "ApiUserController (/api/users)"

api_user_router = APIRouter(prefix="/api/users", tags=[API_TAG])


class ApiUserController:
    """
    API User Controller Class.
    Implements CRUD operations for programmatic REST API client requests.
    """

    # 1. READ ALL (GET /api/users)
    @staticmethod
    def list_users() -> List[User]:
        """CRUD: Read all users from UserModel"""
        return UserModel.get_all()

    # 2. READ BY ID (GET /api/users/{id})
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """CRUD: Read single user by ID from UserModel"""
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
        """CRUD: Create user via UserModel (Status 201 Created)"""
        return UserModel.create(user_data)

    # 4. UPDATE (PUT /api/users/{id})
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """CRUD: Full update of user via UserModel"""
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
        """CRUD: Partial update of user via UserModel"""
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
        """CRUD: Delete user via UserModel"""
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
# Routes: Map /api/users and /api/users/ to ApiUserController
# ---------------------------------------------------------

# GET /api/users and /api/users/
@api_user_router.get("", response_model=List[User], summary="List all users [ApiUserController]")
@api_user_router.get("/", response_model=List[User], include_in_schema=False)
async def get_all_users():
    """Retrieve all users via ApiUserController"""
    return ApiUserController.list_users()


# GET /api/users/{id}
@api_user_router.get("/{id}", response_model=User, summary="Get user by ID [ApiUserController]")
async def get_single_user(id: int):
    """Retrieve a single user by ID via ApiUserController"""
    return ApiUserController.get_user_by_id(id)


# POST /api/users and /api/users/
@api_user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="Create user [ApiUserController]")
@api_user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_user(user_data: UserCreate):
    """Create a new user via ApiUserController"""
    return ApiUserController.create_user(user_data)


# PUT /api/users/{id}
@api_user_router.put("/{id}", response_model=User, summary="Full update user (PUT) [ApiUserController]")
async def update_existing_user(id: int, user_data: UserUpdate):
    """Fully replace an existing user via ApiUserController"""
    return ApiUserController.update_user(id, user_data)


# PATCH /api/users/{id}
@api_user_router.patch("/{id}", response_model=User, summary="Partial update user (PATCH) [ApiUserController]")
async def patch_existing_user(id: int, user_data: UserPatch):
    """Partially update user attributes via ApiUserController"""
    return ApiUserController.patch_user(id, user_data)


# DELETE /api/users/{id}
@api_user_router.delete("/{id}", summary="Delete user [ApiUserController]")
async def remove_user(id: int):
    """Delete a user by ID via ApiUserController"""
    return ApiUserController.delete_user(id)
