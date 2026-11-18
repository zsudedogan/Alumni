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

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text
from middlewares import (
    BodyCheckMiddleware,
    LoggerMiddleware,
    Guardian5xxMiddleware,
    validation_exception_handler,
    custom_starlette_http_exception_handler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist in database
    Base.metadata.create_all(bind=engine)
    # Ensure optional columns like city exist in sqlite if created earlier
    try:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE job_postings ADD COLUMN city VARCHAR(100)"))
            conn.commit()
    except Exception:
        pass
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
4. **Middleware Pipeline**: Request -> Logger -> Read JSON (Body Check) -> Route / Action.
5. **Guardians**: 404 with reason and 5xx guardian error catcher.
    """,
    version="4.1.0",
    docs_url="/api/swagger",      # Swagger UI endpoint requested on whiteboard
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    lifespan=lifespan
)

# ---------------------------------------------------------
# Register Middlewares (Pipeline: 5xx Guardian -> Logger -> BodyCheck -> Route)
# ---------------------------------------------------------
app.add_middleware(BodyCheckMiddleware)
app.add_middleware(LoggerMiddleware)
app.add_middleware(Guardian5xxMiddleware)

# ---------------------------------------------------------
# Register Exception Handlers (400 Validation & 404 Guardian with Reason)
# ---------------------------------------------------------
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, custom_starlette_http_exception_handler)

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



from views.components import get_base_css, render_navbar, render_footer

# ---------------------------------------------------------
# Main Landing Hub (GET /)
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["System"])
async def main_hub():
    """Main Application Landing Hub linking to all interfaces and documentation"""
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Alumni OS - Career & Academic Ecosystem</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}
            .hero-badge {{
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                padding: 0.35rem 0.85rem;
                background: rgba(99, 102, 241, 0.15);
                border: 1px solid rgba(99, 102, 241, 0.35);
                border-radius: 9999px;
                color: #a5b4fc;
                font-size: 0.8rem;
                font-weight: 700;
                margin-bottom: 1.25rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            .hero-badge .dot {{
                width: 8px;
                height: 8px;
                background: #10b981;
                border-radius: 50%;
                box-shadow: 0 0 8px #10b981;
            }}
            .hub-hero {{
                text-align: center;
                max-width: 820px;
                margin: 2.5rem auto 3rem;
            }}
            .hub-hero h1 {{
                font-size: 3rem;
                font-weight: 800;
                line-height: 1.15;
                letter-spacing: -0.03em;
                margin-bottom: 1rem;
                background: linear-gradient(135deg, #ffffff 40%, #94a3b8 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .hub-hero p {{
                font-size: 1.15rem;
                color: var(--text-muted);
                line-height: 1.6;
            }}
            .hub-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 1.5rem;
                margin-bottom: 3rem;
            }}
            .hub-card {{
                background: var(--bg-surface);
                border: 1px solid var(--border-glass);
                border-radius: var(--radius-card);
                padding: 1.75rem;
                backdrop-filter: blur(16px);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
            }}
            .hub-card:hover {{
                transform: translateY(-5px);
                border-color: var(--border-glow);
                box-shadow: 0 15px 30px -10px rgba(99, 102, 241, 0.2);
            }}
            .hub-card-icon {{
                font-size: 2rem;
                margin-bottom: 1rem;
            }}
            .hub-card h2 {{
                font-size: 1.35rem;
                font-weight: 700;
                color: #ffffff;
                margin-bottom: 0.5rem;
            }}
            .hub-card p {{
                color: var(--text-muted);
                font-size: 0.92rem;
                line-height: 1.55;
                margin-bottom: 1.5rem;
                flex-grow: 1;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="")}

        <div class="container">
            <div class="hub-hero">
                <div class="hero-badge">
                    <span class="dot"></span>
                    <span>MVC Lab • Production Ready v4.1</span>
                </div>
                <h1>Unified Alumni & Career Platform</h1>
                <p>High-performance MVC architecture featuring container lifecycle experiments, robust request pipelines, and VoltAgent design standards.</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-label">Architecture</div>
                    <div class="stat-value" style="font-size: 1.6rem; color: #a5b4fc;">MVC + FastAPI</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Request Pipeline</div>
                    <div class="stat-value" style="font-size: 1.6rem; color: #34d399;">Active (Logger)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Guardians</div>
                    <div class="stat-value" style="font-size: 1.6rem; color: #38bdf8;">404 & 5xx Enabled</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Automated Tests</div>
                    <div class="stat-value" style="font-size: 1.6rem; color: #facc15;">21 / 21 Passing</div>
                </div>
            </div>

            <div class="hub-grid">
                <!-- Card 1: Users -->
                <div class="hub-card">
                    <div>
                        <div class="hub-card-icon">👥</div>
                        <h2>User Directory</h2>
                        <p>Browse students, alumni, and recruiters. Supports full CRUD operations, live search, and profile management.</p>
                    </div>
                    <a href="/users/" class="btn btn-primary">Open User View →</a>
                </div>

                <!-- Card 2: Announcements -->
                <div class="hub-card">
                    <div>
                        <div class="hub-card-icon">📢</div>
                        <h2>Department Notices</h2>
                        <p>Publish academic circulars, campus events, and administrative notices with category tags and instant updates.</p>
                    </div>
                    <a href="/announcements/" class="btn btn-secondary">Open Notices View →</a>
                </div>

                <!-- Card 3: Job Postings -->
                <div class="hub-card">
                    <div>
                        <div class="hub-card-icon">💼</div>
                        <h2>Career & Job Postings</h2>
                        <p>Explore internship and full-time opportunities with strict 120-char titles, company validation, and direct application links.</p>
                    </div>
                    <a href="/job-postings/" class="btn btn-primary">Open Career Portal →</a>
                </div>

                <!-- Card 4: Applications -->
                <div class="hub-card">
                    <div>
                        <div class="hub-card-icon">📝</div>
                        <h2>Job Applications</h2>
                        <p>Review candidate submissions, manage application workflows (Pending, Reviewed, Accepted), and submit new applications.</p>
                    </div>
                    <a href="/applications/" class="btn btn-secondary">Open Applications View →</a>
                </div>

                <!-- Card 5: Swagger -->
                <div class="hub-card" style="grid-column: 1 / -1;">
                    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                        <div>
                            <div class="hub-card-icon" style="margin-bottom: 0.5rem;">📖</div>
                            <h2>OpenAPI (Swagger UI) Interactive Documentation</h2>
                            <p style="margin-bottom: 0;">Explore and test all RESTful CRUD endpoints directly in your browser (/api/swagger).</p>
                        </div>
                        <a href="/api/swagger" class="btn btn-primary" target="_blank">Launch Swagger UI ↗</a>
                    </div>
                </div>
            </div>

            {render_footer()}
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
