"""
Classroom Web API - Week 03 Implementation
Full RESTful CRUD API with in-memory storage, health check, and Swagger UI at /api/swagger.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel, EmailStr

# Initialize FastAPI with custom Swagger UI endpoint (/api/swagger as requested on whiteboard item 7)
app = FastAPI(
    title="Classroom REST API - Week 03",
    description="RESTful CRUD API for Users with Health Check and Swagger UI.",
    version="2.0.0",
    docs_url="/api/swagger",      # Whiteboard item 7: GET /api/swagger
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Also redirect standard /docs to /api/swagger for convenience
@app.get("/docs", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/api/swagger")


# ---------------------------------------------------------
# Pydantic Schemas for Users
# ---------------------------------------------------------
class UserBase(BaseModel):
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
    """User response model containing assigned ID"""
    id: int


# ---------------------------------------------------------
# In-Memory Database (Whiteboard item 3: "don't use any database yet")
# ---------------------------------------------------------
users_db: List[User] = [
    User(id=1, name="Emre Yilmaz", age=24, email="emre@example.com"),
    User(id=2, name="Sude Dogan", age=22, email="sude@example.com"),
]
next_user_id: int = 3


# ---------------------------------------------------------
# 1. GET /api/health -> JSON
# ---------------------------------------------------------
@app.get(
    "/api/health",
    summary="1. Health Check",
    tags=["System"]
)
async def health_check():
    """
    Whiteboard item 1:
    GET /api/health -> returns JSON indicating API health status.
    """
    return {
        "status": "UP",
        "message": "API is running healthy",
        "version": "2.0.0"
    }


# ---------------------------------------------------------
# 3. POST /api/users (don't use any database yet)
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
    Whiteboard item 3:
    POST /api/users (in-memory, no database yet).
    Returns the newly created user object with its assigned ID ("what you sent comes back").
    """
    global next_user_id
    new_user = User(id=next_user_id, **user_in.model_dump())
    next_user_id += 1
    users_db.append(new_user)
    return new_user


# ---------------------------------------------------------
# 4. GET /api/users -> list all users
# ---------------------------------------------------------
@app.get(
    "/api/users",
    response_model=List[User],
    summary="4. List All Users",
    tags=["Users"]
)
async def list_users():
    """
    Whiteboard item 4:
    GET /api/users -> returns a list of all existing users.
    """
    return users_db


# ---------------------------------------------------------
# 4b. GET /api/users/{id} -> get user by id
# ---------------------------------------------------------
@app.get(
    "/api/users/{id}",
    response_model=User,
    summary="4b. Get User by ID",
    tags=["Users"]
)
async def get_user_by_id(id: int):
    """
    Whiteboard item 4b:
    GET /api/users/{id} -> returns the user matching the given ID.
    Returns 404 Not Found if user doesn't exist.
    """
    for user in users_db:
        if user.id == id:
            return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id} was not found"
    )


# ---------------------------------------------------------
# 5. PUT /api/users/{id} -> full update
#    PATCH /api/users/{id} -> partial update
# ---------------------------------------------------------
@app.put(
    "/api/users/{id}",
    response_model=User,
    summary="5. Full Update User (PUT)",
    tags=["Users"]
)
async def update_user_put(id: int, user_in: UserUpdate):
    """
    Whiteboard item 5:
    PUT /api/users/{id} -> replaces all fields of the specified user.
    """
    for index, user in enumerate(users_db):
        if user.id == id:
            updated_user = User(id=id, **user_in.model_dump())
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id} was not found"
    )


@app.patch(
    "/api/users/{id}",
    response_model=User,
    summary="5. Partial Update User (PATCH)",
    tags=["Users"]
)
async def update_user_patch(id: int, user_in: UserPatch):
    """
    Whiteboard item 5:
    PATCH /api/users/{id} -> updates only the provided fields of the user.
    """
    for index, user in enumerate(users_db):
        if user.id == id:
            stored_data = user.model_dump()
            update_data = user_in.model_dump(exclude_unset=True)
            stored_data.update(update_data)
            updated_user = User(**stored_data)
            users_db[index] = updated_user
            return updated_user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id} was not found"
    )


# ---------------------------------------------------------
# 6. DELETE /api/users/{id}
# ---------------------------------------------------------
@app.delete(
    "/api/users/{id}",
    summary="6. Delete User",
    tags=["Users"]
)
async def delete_user(id: int):
    """
    Whiteboard item 6:
    DELETE /api/users/{id} -> removes user with matching ID from memory.
    """
    for index, user in enumerate(users_db):
        if user.id == id:
            removed_user = users_db.pop(index)
            return {
                "message": f"User with ID {id} has been successfully deleted",
                "deleted_user": removed_user
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User with ID {id} was not found"
    )


# ---------------------------------------------------------
# Previous Week Routes (Preserved for Reference & Testing)
# ---------------------------------------------------------
@app.get("/", response_class=PlainTextResponse, tags=["Week 02 Reference"])
async def root():
    return "ok"

@app.get("/hello", response_class=PlainTextResponse, tags=["Week 02 Reference"])
async def say_hello():
    return "Hello, World!"

@app.get("/hello/{name}", response_class=PlainTextResponse, tags=["Week 02 Reference"])
async def say_hello_name(name: str):
    return f"Hello, {name.strip().capitalize()}!"

@app.get("/sum/{number1}/{number2}", tags=["Week 02 Reference"])
async def calculate_sum(number1: int, number2: int):
    return {"number1": number1, "number2": number2, "sum": number1 + number2}


# ---------------------------------------------------------
# Server Launch
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
