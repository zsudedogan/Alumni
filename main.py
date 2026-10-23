"""
Classroom Web API - Complete MVC Architecture Implementation
Mounts User and Announcement Controllers (both Web/View and API/JSON) and configures Swagger UI.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse

# Import Controllers and Routers
from controllers.api_user_controller import api_user_router, ApiUserController
from controllers.user_controller import user_router, UserController
from controllers.api_announcement_controller import api_announcement_router, ApiAnnouncementController
from controllers.announcement_controller import announcement_router, AnnouncementController
from controllers.api_job_posting_controller import (
    api_job_posting_router,
    nested_job_posting_router,
    ApiJobPostingController,
)
from controllers.job_posting_controller import job_posting_router, JobPostingController
from controllers.api_application_controller import (
    api_application_router,
    nested_job_application_router,
    nested_user_application_router,
    ApiApplicationController,
)
from controllers.application_controller import application_router, ApplicationController

# ---------------------------------------------------------
# Swagger (OpenAPI) Tag Metadata
# ---------------------------------------------------------
tags_metadata = [
    {
        "name": "ApiUserController (/api/users)",
        "description": "RESTful CRUD API endpoints for programmatic User operations (JSON format).",
    },
    {
        "name": "UserController (/users)",
        "description": "User Controller with **View Layer** (HTML Management Interface) for listing (R), creating (C), updating, and deleting users.",
    },
    {
        "name": "ApiAnnouncementController (/api/announcements)",
        "description": "RESTful CRUD API endpoints for programmatic Announcement operations (JSON format).",
    },
    {
        "name": "AnnouncementController (/announcements)",
        "description": "Announcement Controller with **View Layer** (HTML Management Interface) to manage announcements.",
    },
    {
        "name": "ApiJobPostingController (/api/job-postings)",
        "description": "**Direct Routes**: Full CRUD operations for Job Postings (/api/job-postings).",
    },
    {
        "name": "Nested Routes: Users -> JobPostings (/api/users/{user_id}/job-postings)",
        "description": "**Nested Routes**: Demonstrates 1-to-many relationship endpoints (/api/users/{user_id}/job-postings).",
    },
    {
        "name": "JobPostingController (/job-postings)",
        "description": "Job Posting Controller with **View Layer** (HTML Management Interface).",
    },
    {
        "name": "ApiApplicationController (/api/applications)",
        "description": "**Direct Routes**: Full CRUD operations for Job Applications (/api/applications).",
    },
    {
        "name": "Nested Routes: JobPostings -> Applications (/api/job-postings/{job_id}/applications)",
        "description": "**Nested Routes**: Submit and list applications under a specific job posting.",
    },
    {
        "name": "Nested Routes: Users -> Applications (/api/users/{user_id}/applications)",
        "description": "**Nested Routes**: View and manage applications submitted by a specific user.",
    },
    {
        "name": "ApplicationController (/applications)",
        "description": "Application Controller with **View Layer** (HTML Management Interface).",
    },
    {
        "name": "System",
        "description": "System health and diagnostics endpoint (`/api/health`).",
    },
    {
        "name": "Reference",
        "description": "Previous week reference routes (`/hello`, `/hello/{name}`).",
    },
]

from contextlib import asynccontextmanager
from database import engine, Base
import models.db_entities

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist in database
    Base.metadata.create_all(bind=engine)
    yield

# Initialize FastAPI application with custom Swagger UI at /api/swagger
app = FastAPI(
    title="Classroom REST API - Full MVC Architecture",
    description="""
## 🎓 Classroom MVC Architecture API
Complete implementation of:
1. **User Module**: `UserController` (`/users/` with View Layer) & `ApiUserController` (`/api/users/`)
2. **Announcement Module (Homework)**: `AnnouncementController` (`/announcements/` with View Layer) & `ApiAnnouncementController` (`/api/announcements/`)
3. **Database CRUD Persistence**: Connected to PostgreSQL/SQLite via SQLAlchemy & Alembic.
    """,
    version="4.0.0",
    docs_url="/api/swagger",      # Swagger UI endpoint requested on whiteboard
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# Redirect standard /docs to /api/swagger
@app.get("/docs", include_in_schema=False)
async def redirect_to_swagger():
    return RedirectResponse(url="/api/swagger")



# ---------------------------------------------------------
# Register Routers (MVC Architecture)
# ---------------------------------------------------------
# User Module
app.include_router(api_user_router)
app.include_router(user_router)

# Announcement Module (Homework)
app.include_router(api_announcement_router)
app.include_router(announcement_router)

# Job Posting Module (Direct & Nested Routes)
app.include_router(api_job_posting_router)
app.include_router(nested_job_posting_router)
app.include_router(job_posting_router)

# Application Module (Direct & Nested Routes)
app.include_router(api_application_router)
app.include_router(nested_job_application_router)
app.include_router(nested_user_application_router)
app.include_router(application_router)



# ---------------------------------------------------------
# Main Landing Hub (GET /)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["System"])
async def main_hub():
    """Main Application Landing Hub linking to all interfaces and documentation"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Classroom MVC API Hub</title>
        <style>
            :root {
                --primary: #4f46e5;
                --bg: #0f172a;
                --card-bg: #1e293b;
                --text: #f8fafc;
                --muted: #94a3b8;
                --accent: #38bdf8;
                --border: #334155;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background-color: var(--bg);
                color: var(--text);
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 2rem 1rem;
            }
            .container { max-width: 860px; width: 100%; }
            .hero { text-align: center; margin-bottom: 2.5rem; }
            .hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #818cf8, #38bdf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            .hero p { color: var(--muted); font-size: 1.1rem; }
            .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 1.5rem; }
            .card {
                background: var(--card-bg);
                border: 1px solid var(--border);
                border-radius: 14px;
                padding: 1.75rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 0.2s, border-color 0.2s;
            }
            .card:hover { transform: translateY(-4px); border-color: var(--accent); }
            .card h2 { font-size: 1.3rem; margin-bottom: 0.5rem; color: #ffffff; }
            .card p { color: var(--muted); font-size: 0.9rem; margin-bottom: 1.5rem; line-height: 1.5; flex-grow: 1; }
            .btn {
                display: block;
                text-align: center;
                padding: 0.75rem 1rem;
                background: var(--primary);
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: 600;
                font-size: 0.95rem;
                transition: background 0.2s;
            }
            .btn:hover { background: #4338ca; }
            .btn-alt { background: #0284c7; }
            .btn-alt:hover { background: #0369a1; }
            .btn-docs { background: #059669; }
            .btn-docs:hover { background: #047857; }
            .badge { display: inline-block; padding: 0.2rem 0.5rem; font-size: 0.75rem; border-radius: 4px; background: rgba(56, 189, 248, 0.15); color: var(--accent); margin-bottom: 0.75rem; }
            footer { text-align: center; margin-top: 3rem; color: #64748b; font-size: 0.85rem; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🏛️ Classroom MVC Application Hub</h1>
                <p>Model-View-Controller Architecture: Web Views, CRUD Controllers & REST APIs</p>
            </div>

            <div class="grid">
                <!-- Card 1: Users -->
                <div class="card">
                    <div>
                        <span class="badge">Whiteboard 5 & 6</span>
                        <h2>👥 Users Management</h2>
                        <p>Web interface for listing (R) and creating (C) users with full in-memory CRUD operations and View Layer.</p>
                    </div>
                    <a href="/users/" class="btn">Open Users View</a>
                </div>

                <!-- Card 2: Announcements (Homework) -->
                <div class="card">
                    <div>
                        <span class="badge">Homework Assignment</span>
                        <h2>📢 Announcements</h2>
                        <p>Complete announcement management interface without database: create, read, update, delete.</p>
                    </div>
                    <a href="/announcements/" class="btn btn-alt">Open Announcements View</a>
                </div>

                <!-- Card 3: Job Postings -->
                <div class="card">
                    <div>
                        <span class="badge">Direct & Nested Routes</span>
                        <h2>💼 Career & Job Postings</h2>
                        <p>Explore opportunities or publish listings. Supports direct routes and nested user-resource relationships.</p>
                    </div>
                    <a href="/job-postings/" class="btn" style="background: #0284c7;">Open Job Postings View</a>
                </div>

                <!-- Card 4: Applications -->
                <div class="card">
                    <div>
                        <span class="badge">Direct & Nested Routes</span>
                        <h2>📝 Job Applications</h2>
                        <p>Track and manage student applications. Nested under job postings and users with full CRUD operations.</p>
                    </div>
                    <a href="/applications/" class="btn" style="background: #7c3aed;">Open Applications View</a>
                </div>

                <!-- Card 5: Swagger UI -->
                <div class="card">
                    <div>
                        <span class="badge">OpenAPI Documentation</span>
                        <h2>📖 Swagger API Docs</h2>
                        <p>Interactive OpenAPI documentation for all controllers (Users, Announcements, Job Postings, Applications).</p>
                    </div>
                    <a href="/api/swagger" class="btn btn-docs" target="_blank">Launch Swagger UI</a>
                </div>
            </div>

            <footer>
                Department of Management Information Systems • Istanbul University of Economics • MVC Lab
            </footer>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


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
        "message": "Classroom MVC API is running healthy",
        "modules": ["Users", "Announcements"],
        "architecture": "MVC (Model, View, Controller)",
        "swagger_docs": "/api/swagger"
    }


# ---------------------------------------------------------
# Reference Endpoints (Week 02)
# ---------------------------------------------------------
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
