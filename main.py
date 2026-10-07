"""
Classroom Web API - MVC Architecture Implementation
Controller layer coordinating routes, using the User Model for CRUD operations.
"""

from typing import List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import PlainTextResponse, RedirectResponse

# Import User Model and Schemas from Model Layer
from models.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPatch,
    UserModel
)

# Initialize FastAPI with custom Swagger UI endpoint (/api/swagger)
app = FastAPI(
    title="Classroom REST API - MVC Architecture",
    description="RESTful CRUD API for Users built with MVC Pattern and Swagger UI.",
    version="3.0.0",
    docs_url="/api/swagger",      # Swagger UI endpoint
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Redirect standard /docs to /api/swagger
@app.get("/docs", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/api/swagger")


# ---------------------------------------------------------
# 1. GET /api/health -> JSON
# ---------------------------------------------------------
@app.get(
    "/api/health",
    summary="1. Health Check",
    tags=["System"]
)
async def health_check():
    """Returns API health status"""
    return {
        "status": "UP",
        "message": "API is running healthy",
        "architecture": "MVC"
    }


# ---------------------------------------------------------
# 3. POST /api/users -> Create User (Model CRUD: create)
# ---------------------------------------------------------
@app.post(
    "/api/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="3. Create User",
    tags=["Users"]
)
async def create_user(user_in: UserCreate):
    """
    Controller: Delegates user creation to UserModel.create()
    """
    new_user = UserModel.create(user_in)
    return new_user


# ---------------------------------------------------------
# 4. GET /api/users -> List All Users (Model CRUD: get_all)
# ---------------------------------------------------------
@app.get(
    "/api/users",
    response_model=List[User],
    summary="4. List All Users",
    tags=["Users"]
)
async def list_users():
    """
    Controller: Delegates retrieval of all users to UserModel.get_all()
    """
    return UserModel.get_all()


# ---------------------------------------------------------
# 4b. GET /api/users/{id} -> Get User by ID (Model CRUD: get_by_id)
# ---------------------------------------------------------
@app.get(
    "/api/users/{id}",
    response_model=User,
    summary="4b. Get User by ID",
    tags=["Users"]
)
async def get_user_by_id(id: int):
    """
    Controller: Delegates finding user by ID to UserModel.get_by_id()
    """
    user = UserModel.get_by_id(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} was not found"
        )
    return user


# ---------------------------------------------------------
# 5. PUT /api/users/{id} -> Full Update (Model CRUD: update)
# ---------------------------------------------------------
@app.put(
    "/api/users/{id}",
    response_model=User,
    summary="5. Full Update User (PUT)",
    tags=["Users"]
)
async def update_user_put(id: int, user_in: UserUpdate):
    """
    Controller: Delegates full user update to UserModel.update()
    """
    updated_user = UserModel.update(id, user_in)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} was not found"
        )
    return updated_user


# ---------------------------------------------------------
# 5. PATCH /api/users/{id} -> Partial Update (Model CRUD: patch)
# ---------------------------------------------------------
@app.patch(
    "/api/users/{id}",
    response_model=User,
    summary="5. Partial Update User (PATCH)",
    tags=["Users"]
)
async def update_user_patch(id: int, user_in: UserPatch):
    """
    Controller: Delegates partial user update to UserModel.patch()
    """
    patched_user = UserModel.patch(id, user_in)
    if not patched_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} was not found"
        )
    return patched_user


# ---------------------------------------------------------
# 6. DELETE /api/users/{id} -> Delete User (Model CRUD: delete)
# ---------------------------------------------------------
@app.delete(
    "/api/users/{id}",
    summary="6. Delete User",
    tags=["Users"]
)
async def delete_user(id: int):
    """
    Controller: Delegates user deletion to UserModel.delete()
    """
    deleted_user = UserModel.delete(id)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {id} was not found"
        )
    return {
        "message": f"User with ID {id} has been successfully deleted",
        "deleted_user": deleted_user
    }


# ---------------------------------------------------------
# Reference Endpoints (Week 02)
# ---------------------------------------------------------
@app.get("/", response_class=PlainTextResponse, tags=["Reference"])
async def root():
    return "ok"

@app.get("/hello", response_class=PlainTextResponse, tags=["Reference"])
async def say_hello():
    return "Hello, World!"

@app.get("/hello/{name}", response_class=PlainTextResponse, tags=["Reference"])
async def say_hello_name(name: str):
    return f"Hello, {name.strip().capitalize()}!"


# ---------------------------------------------------------
# Server Launch
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
