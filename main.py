"""
Classroom Web API - MVC Architecture Implementation
Main application module incorporating UserController and ApiUserController.
Configures comprehensive Swagger UI documentation at /api/swagger.
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse

# Import Controllers and Routers
from controllers.api_user_controller import api_user_router, ApiUserController
from controllers.user_controller import user_router, UserController

# ---------------------------------------------------------
# Swagger (OpenAPI) Tag Metadata
# ---------------------------------------------------------
tags_metadata = [
    {
        "name": "ApiUserController (/api/users)",
        "description": "Endpoints mapped to **ApiUserController**. Handles programmatic REST API requests (`.../api/users` and `.../api/users/`) with JSON responses and standard HTTP status codes.",
    },
    {
        "name": "UserController (/users)",
        "description": "Endpoints mapped to **UserController**. Handles core application and web user requests (`.../users` and `.../users/`).",
    },
    {
        "name": "System",
        "description": "System health and status endpoints (`/api/health`).",
    },
    {
        "name": "Reference",
        "description": "Week 02 reference endpoints (`/`, `/hello`, `/hello/{name}`).",
    },
]

# Initialize FastAPI application with custom Swagger UI at /api/swagger
app = FastAPI(
    title="Classroom REST API - MVC Architecture",
    description="""
## 🎓 Classroom MVC Architecture API
Implementation of **UserController** (`.../users/`) and **ApiUserController** (`.../api/users/`) 
following the **Model-View-Controller (MVC)** architectural design.

### 📌 Architecture Mapping:
* **Model**: [`models/user.py`](./models/user.py) (`UserModel` with in-memory CRUD operations)
* **Controllers**:
  * **`UserController`**: Mapped to routes starting with `.../users/`
  * **`ApiUserController`**: Mapped to routes starting with `.../api/users/`
* **View / Documentation**: Swagger UI at `/api/swagger` & JSON serialization
    """,
    version="3.3.0",
    docs_url="/api/swagger",      # Swagger UI endpoint requested on whiteboard
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata
)

# Redirect standard /docs to /api/swagger
@app.get("/docs", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/api/swagger")


# ---------------------------------------------------------
# Register Controllers (MVC Routing)
# ---------------------------------------------------------
# 1. ApiUserController handling .../api/users and .../api/users/
app.include_router(api_user_router)

# 2. UserController handling .../users and .../users/
app.include_router(user_router)


# ---------------------------------------------------------
# System Health Check Endpoint
# ---------------------------------------------------------
@app.get(
    "/api/health",
    summary="Health Check",
    tags=["System"]
)
async def health_check():
    """Returns API health status"""
    return {
        "status": "UP",
        "message": "API is running healthy",
        "architecture": "MVC (UserController & ApiUserController)",
        "swagger_docs": "/api/swagger"
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
