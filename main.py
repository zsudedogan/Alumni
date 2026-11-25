"""
Classroom Web API - Complete MVC Architecture Implementation
Mounts User and Announcement Controllers (both Web/View and API/JSON) and configures Swagger UI.
"""

from fastapi import FastAPI, Request
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
from controllers.register_controller import register_router
from controllers.auth_controller import auth_router
from controllers.admin_controller import admin_router
from controllers.portal_controller import portal_router

# ---------------------------------------------------------
# Swagger (OpenAPI) Tag Metadata
# ---------------------------------------------------------
tags_metadata = [
    {
        "name": "Authentication & Registration",
        "description": "User registration portal (`/register/`) and account onboarding (`/api/auth/register`) with ecosystem roles.",
    },
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
    AuthMiddleware,
    validation_exception_handler,
    custom_starlette_http_exception_handler,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist in database
    Base.metadata.create_all(bind=engine)
    # Ensure optional columns exist in sqlite if created earlier
    with engine.connect() as conn:
        for alter_stmt in [
            "ALTER TABLE job_postings ADD COLUMN city VARCHAR(100)",
            "ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'Student'",
            "ALTER TABLE users ADD COLUMN department VARCHAR(100)",
            "ALTER TABLE users ADD COLUMN bio TEXT",
            "ALTER TABLE users ADD COLUMN password VARCHAR(255)",
            "ALTER TABLE users ADD COLUMN created_at VARCHAR(20)",
        ]:
            try:
                conn.execute(text(alter_stmt))
                conn.commit()
            except Exception:
                pass
        # Ensure Sude Dogan (id 2) has role='Admin' and password
        try:
            conn.execute(text("UPDATE users SET role='Admin', password='password123' WHERE id=2"))
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
# Register Middlewares (Pipeline: 5xx Guardian -> Logger -> Auth -> BodyCheck -> Route)
# ---------------------------------------------------------
app.add_middleware(BodyCheckMiddleware)
app.add_middleware(AuthMiddleware)
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

# Authentication & Registration Module
app.include_router(register_router)
app.include_router(auth_router)

# Administrative Control Center Module
app.include_router(admin_router)

# User Role Portals Module
app.include_router(portal_router)



from views.components import get_base_css, render_navbar, render_footer, render_iu_logo

# ---------------------------------------------------------
# Main Landing Hub (GET /) - UniBridge Giriş Sistemi
# ---------------------------------------------------------
@app.get("/", response_class=HTMLResponse, tags=["System"])
async def main_hub(request: Request):
    """UniBridge Istanbul University Entry & Career Portal"""
    current_user = getattr(request.state, "user", None)
    admin_banner_html = ""
    if current_user and getattr(current_user, "role", "") == "Admin":
        admin_banner_html = f"""
        <div style="background: rgba(197, 155, 39, 0.12); border: 1px solid rgba(197, 155, 39, 0.35); border-radius: 12px; padding: 1.1rem 1.6rem; margin-bottom: 2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; box-shadow: 0 4px 15px rgba(197, 155, 39, 0.1);">
            <div style="display: flex; align-items: center; gap: 0.85rem;">
                <span style="font-size: 1.8rem;">👑</span>
                <div>
                    <div style="font-weight: 800; color: #854d0e; font-size: 1.05rem;">Yönetici Girişi Yapıldı: {current_user.name} (Admin)</div>
                    <div style="font-size: 0.85rem; color: #78350f;">UniBridge Yönetim Paneli üzerinden kullanıcıları, duyuruları ve ilanları manipüle edebilirsiniz.</div>
                </div>
            </div>
            <a href="/admin/" class="btn btn-primary" style="background: var(--primary); padding: 0.6rem 1.2rem; font-size: 0.9rem;">Yönetim Paneline Git →</a>
        </div>
        """
    html = f"""
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>UniBridge Giriş Sistemi • İstanbul Üniversitesi</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
        <style>
            {get_base_css()}

            .unibridge-hero {{
                text-align: center;
                margin: 2rem auto 2.5rem;
                display: flex;
                flex-direction: column;
                align-items: center;
                gap: 0.85rem;
            }}

            .unibridge-hero h1 {{
                font-size: 2.25rem;
                font-weight: 800;
                color: var(--primary);
                letter-spacing: -0.02em;
                margin: 0;
            }}

            .unibridge-hero p {{
                color: var(--text-muted);
                font-size: 1.05rem;
                margin: 0;
                font-weight: 500;
            }}

            /* UniBridge Role Cards Layout */
            .portal-cards-wrapper {{
                max-width: 580px;
                margin: 0 auto 3.5rem;
                display: flex;
                flex-direction: column;
                gap: 1.75rem;
            }}

            .unibridge-card {{
                background: #ffffff;
                border: 1px solid var(--border-card);
                border-radius: var(--radius-card);
                padding: 2.25rem 2rem 2rem;
                box-shadow: var(--shadow-card);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                transition: transform 0.25s, box-shadow 0.25s;
            }}

            .unibridge-card:hover {{
                transform: translateY(-3px);
                box-shadow: var(--shadow-elevated);
            }}

            .icon-circle {{
                width: 60px;
                height: 60px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.75rem;
                margin-bottom: 1.25rem;
            }}

            .icon-student {{ background: #e8f3fc; color: #1d4ed8; }}
            .icon-alumni {{ background: #fef6e7; color: #c59b27; }}
            .icon-academic {{ background: #ede9fe; color: #6b21a8; }}
            .icon-recruiter {{ background: #e6f4ea; color: #15803d; }}

            .unibridge-card h2 {{
                font-size: 1.4rem;
                font-weight: 800;
                color: var(--primary);
                margin-bottom: 0.5rem;
            }}

            .unibridge-card p {{
                color: var(--text-muted);
                font-size: 0.95rem;
                margin-bottom: 1.5rem;
                max-width: 420px;
                line-height: 1.5;
            }}

            .btn-unibridge {{
                width: 100%;
                max-width: 440px;
                padding: 0.95rem 1.5rem;
                font-size: 1.05rem;
                font-weight: 700;
                border-radius: 14px;
                background: var(--primary);
                color: #ffffff !important;
                border: none;
                cursor: pointer;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                transition: background 0.2s, transform 0.2s, box-shadow 0.2s;
                box-shadow: 0 4px 12px var(--primary-glow);
            }}

            .btn-unibridge:hover {{
                background: var(--primary-dark);
                transform: translateY(-1px);
                box-shadow: 0 6px 16px var(--primary-glow);
            }}

            /* Quick Access Modules Grid */
            .modules-section {{
                border-top: 1px solid var(--border-glass);
                padding-top: 3rem;
                margin-top: 1rem;
            }}

            .modules-header {{
                text-align: center;
                margin-bottom: 2rem;
            }}

            .modules-header h3 {{
                font-size: 1.4rem;
                font-weight: 800;
                color: var(--primary);
                margin-bottom: 0.3rem;
            }}

            .modules-header p {{
                color: var(--text-muted);
                font-size: 0.95rem;
            }}

            .modules-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
                gap: 1.25rem;
            }}

            .module-card {{
                background: #ffffff;
                border: 1px solid var(--border-card);
                border-radius: var(--radius-card);
                padding: 1.5rem;
                box-shadow: var(--shadow-card);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                transition: transform 0.2s;
            }}

            .module-card:hover {{
                transform: translateY(-2px);
                border-color: rgba(32, 71, 41, 0.2);
            }}

            .module-card h4 {{
                font-size: 1.1rem;
                font-weight: 800;
                color: var(--primary);
                margin-bottom: 0.4rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }}

            .module-card p {{
                color: var(--text-muted);
                font-size: 0.88rem;
                line-height: 1.5;
                margin-bottom: 1.25rem;
                flex-grow: 1;
            }}
        </style>
    </head>
    <body>
        {render_navbar(active_route="home", current_user=current_user)}

        <div class="container">
            {admin_banner_html}
            <!-- Top Official Seal & UniBridge Header -->
            <div class="unibridge-hero">
                {render_iu_logo(size=92)}
                <h1>UniBridge Giriş Sistemi</h1>
                <p>Lütfen devam etmek için kullanıcı tipinizi seçin</p>
            </div>

            <!-- UniBridge Role Selection Cards (Matches Reference PDF) -->
            <div class="portal-cards-wrapper">
                <!-- 1. Öğrenci -->
                <div class="unibridge-card">
                    <div class="icon-circle icon-student">🎓</div>
                    <h2>Öğrenci</h2>
                    <p>Aktif öğrenciler için öğrenci otomasyonu girişi.</p>
                    <a href="/portal/student" class="btn-unibridge">Portala Git →</a>
                </div>

                <!-- 2. Mezun -->
                <div class="unibridge-card">
                    <div class="icon-circle icon-alumni">🎖️</div>
                    <h2>Mezun</h2>
                    <p>Mezunlar ağı ve kariyer fırsatları portalı.</p>
                    <a href="/portal/alumni" class="btn-unibridge">Portala Git →</a>
                </div>

                <!-- 3. Akademik -->
                <div class="unibridge-card">
                    <div class="icon-circle icon-academic">🖥️</div>
                    <h2>Akademik</h2>
                    <p>Öğretim üyeleri ve idari personel erişimi.</p>
                    <a href="/portal/academic" class="btn-unibridge">Portala Git →</a>
                </div>

                <!-- 4. İşveren / İK -->
                <div class="unibridge-card">
                    <div class="icon-circle icon-recruiter">🏢</div>
                    <h2>İşveren / Sektör</h2>
                    <p>Kurumsal iş ve staj ilanları yönetimi ile aday değerlendirme portalı.</p>
                    <a href="/portal/recruiter" class="btn-unibridge">Portala Git →</a>
                </div>
            </div>

            <!-- Quick Access Modules & Swagger UI -->
            <div class="modules-section">
                <div class="modules-header">
                    <h3>⚡ Sistem Portalları & Hızlı Erişim</h3>
                    <p>Alumni Ekosistemi yönetim arayüzleri ve geliştirici araçları</p>
                </div>

                <div class="modules-grid">
                    <div class="module-card">
                        <div>
                            <h4>👥 Kullanıcı Rehberi</h4>
                            <p>Öğrenci, mezun ve akademik kullanıcı listesi ve profil yönetimi.</p>
                        </div>
                        <a href="/users/" class="btn btn-secondary btn-sm">Görüntüle →</a>
                    </div>

                    <div class="module-card">
                        <div>
                            <h4>📢 Bölüm Duyuruları</h4>
                            <p>Akademik duyurular, staj ilanları ve idari bildirimler.</p>
                        </div>
                        <a href="/announcements/" class="btn btn-secondary btn-sm">Duyurular →</a>
                    </div>

                    <div class="module-card">
                        <div>
                            <h4>💼 Kariyer Portalı</h4>
                            <p>Şirket iş ilanları, staj pozisyonları ve başvuru olanakları.</p>
                        </div>
                        <a href="/job-postings/" class="btn btn-secondary btn-sm">İlanlar →</a>
                    </div>

                    <div class="module-card">
                        <div>
                            <h4>📝 Başvuru Yönetimi</h4>
                            <p>İş ve staj başvurularını inceleme ve statü onay takip paneli.</p>
                        </div>
                        <a href="/applications/" class="btn btn-secondary btn-sm">Başvurular →</a>
                    </div>

                    <div class="module-card" style="grid-column: 1 / -1; background: #fafcfb; border-color: rgba(197, 155, 39, 0.35);">
                        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                            <div>
                                <h4 style="color: var(--primary);">📖 OpenAPI (Swagger UI) Geliştirici Dokümantasyonu</h4>
                                <p style="margin-bottom: 0;">Sistem RESTful CRUD API uç noktalarını tarayıcı üzerinden interaktif olarak test edin.</p>
                            </div>
                            <a href="/api/swagger" target="_blank" class="btn btn-primary btn-sm">Swagger UI Aç ↗</a>
                        </div>
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
