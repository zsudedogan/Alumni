"""
Classroom Web API - MVC Architecture Implementation
Main application module incorporating UserController and ApiUserController.
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, RedirectResponse

# Import Controllers and Routers
from controllers.api_user_controller import api_user_router, ApiUserController
from controllers.user_controller import user_router, UserController

# Initialize FastAPI application with custom Swagger UI at /api/swagger
app = FastAPI(
    title="Classroom REST API - MVC Architecture",
    description="RESTful CRUD API for Users built with MVC Pattern (UserController & ApiUserController).",
    version="3.1.0",
    docs_url="/api/swagger",      # Swagger UI endpoint
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Redirect standard /docs to /api/swagger
@app.get("/docs", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/api/swagger")


# ---------------------------------------------------------
# Register Controllers (MVC Routing)
# ---------------------------------------------------------
# 1. ApiUserController handling /api/users
app.include_router(api_user_router)

# 2. UserController handling /users
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
        "architecture": "MVC (UserController & ApiUserController)"
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
