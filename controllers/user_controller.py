"""
UserController - MVC Architecture
Controller dedicated to handling User routes (/users and /users/) WITH VIEW LAYER.
Implements Whiteboard Items 5 & 6:
- 5: GET .../users -> listing (R), POST .../users -> creating (C), define 2 routes with view layer
- 6: Define all CRUD operations on user route and controller with view
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from models.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPatch,
    UserModel
)
from views.user_view import render_user_management_page

USER_TAG = "UserController (/users)"

user_router = APIRouter(prefix="/users", tags=[USER_TAG])


class UserController:
    """
    Standard User Controller Class with View Layer.
    Implements core application CRUD logic and connects to the View Layer.
    """

    # 1. READ ALL / VIEW INTERFACE (GET /users)
    @staticmethod
    def render_interface() -> HTMLResponse:
        """CRUD (Read/Listing - R): Render HTML View Layer management page"""
        users = UserModel.get_all()
        html = render_user_management_page(users)
        return HTMLResponse(content=html)

    @staticmethod
    def list_users() -> List[User]:
        """CRUD (Read/Listing - R): Retrieve user entities list"""
        return UserModel.get_all()

    # 2. READ BY ID (GET /users/{id})
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """CRUD (Read - R): Retrieve a user by ID"""
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
        """CRUD (Creating - C): Create user via UserModel"""
        return UserModel.create(user_data)

    # 4. UPDATE (PUT /users/{id})
    @staticmethod
    def update_user(user_id: int, user_data: UserUpdate) -> User:
        """CRUD (Updating - U): Full update of user attributes"""
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
        """CRUD (Updating - U): Partial update of user attributes"""
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
        """CRUD (Deleting - D): Remove user from memory"""
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
# Routes with View Layer (Whiteboard Items 5 & 6)
# ---------------------------------------------------------

# 5. GET .../users -> listing (R) with View Layer (HTML page)
@user_router.get("", response_class=HTMLResponse, summary="5. User Management Interface (View Layer) [UserController]")
@user_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_user_management_interface():
    """Whiteboard Item 5: GET .../users -> listing (R) with view layer"""
    return UserController.render_interface()


# GET .../users/data -> raw JSON data for user list
@user_router.get("/data", response_model=List[User], summary="Get raw users JSON list [UserController]")
async def get_raw_users():
    return UserController.list_users()


# GET .../users/{id}
@user_router.get("/{id}", response_model=User, summary="6. Get user by ID [UserController]")
async def get_single_user(id: int):
    return UserController.get_user_by_id(id)


# 5. POST .../users -> creating (C)
@user_router.post("", response_model=User, status_code=status.HTTP_201_CREATED, summary="5. Create user (C) [UserController]")
@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_user(user_data: UserCreate):
    """Whiteboard Item 5: POST .../users -> creating (C)"""
    return UserController.create_user(user_data)


# 6. PUT .../users/{id} -> Full update
@user_router.put("/{id}", response_model=User, summary="6. Full update user (PUT) [UserController]")
async def update_existing_user(id: int, user_data: UserUpdate):
    """Whiteboard Item 6: PUT user with view / controller"""
    return UserController.update_user(id, user_data)


# 6. PATCH .../users/{id} -> Partial update
@user_router.patch("/{id}", response_model=User, summary="6. Partial update user (PATCH) [UserController]")
async def patch_existing_user(id: int, user_data: UserPatch):
    """Whiteboard Item 6: PATCH user with view / controller"""
    return UserController.patch_user(id, user_data)


# 6. DELETE .../users/{id} -> Delete
@user_router.delete("/{id}", summary="6. Delete user [UserController]")
async def remove_user(id: int):
    """Whiteboard Item 6: DELETE user with view / controller"""
    return UserController.delete_user(id)
