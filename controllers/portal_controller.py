"""
Portal Controller - MVC Architecture
Serves user-specific pages and personalized workspaces for Student, Alumni, Recruiter, and Academic roles.
"""

from typing import Optional
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from models.user import get_all_user_records, User
from models.job_posting import get_all_job_posting_records
from models.application import get_all_application_records
from models.announcement import get_all_announcement_records
from middlewares.auth import get_current_user_from_request
from views.portal_views import (
    render_student_portal,
    render_alumni_portal,
    render_recruiter_portal,
    render_academic_portal,
)

portal_router = APIRouter(tags=["User Role Portals"])


def _resolve_or_mock_user(request: Request, required_role: str = "Student") -> User:
    """Helper to get logged-in user or provide a representative persona for portal preview"""
    user = getattr(request.state, "user", None)
    if not user:
        user = get_current_user_from_request(request)

    if user:
        return user

    # If unauthenticated, find or build a default representative persona
    all_users = get_all_user_records()
    matching_user = next((u for u in all_users if u.role == required_role), None)
    if matching_user:
        return matching_user

    return User(
        id=0,
        name=f"Konuk {required_role}",
        email=f"guest_{required_role.lower()}@istanbul.edu.tr",
        role=required_role,
        department="Yönetim Bilişim Sistemleri"
    )


# ---------------------------------------------------------
# Dynamic Universal Portal Hub (GET /portal/ and /portal)
# ---------------------------------------------------------
@portal_router.get("/portal/", response_class=HTMLResponse, summary="Universal Portal Router")
def dynamic_portal_hub(request: Request):
    """Automatically routes the user to their role-specific portal"""
    current_user = getattr(request.state, "user", None) or get_current_user_from_request(request)

    if not current_user:
        return RedirectResponse(url="/login/?next=/portal/", status_code=303)

    role = current_user.role
    if role == "Admin":
        return RedirectResponse(url="/admin/", status_code=303)
    elif role == "Student":
        return RedirectResponse(url="/portal/student", status_code=303)
    elif role == "Alumni":
        return RedirectResponse(url="/portal/alumni", status_code=303)
    elif role == "Recruiter":
        return RedirectResponse(url="/portal/recruiter", status_code=303)
    elif role == "Academic":
        return RedirectResponse(url="/portal/academic", status_code=303)

    return RedirectResponse(url="/", status_code=303)


@portal_router.get("/portal", response_class=HTMLResponse, include_in_schema=False)
def dynamic_portal_hub_no_slash(request: Request):
    return dynamic_portal_hub(request)


# ---------------------------------------------------------
# 1. Student Portal (GET /portal/student)
# ---------------------------------------------------------
@portal_router.get("/portal/student", response_class=HTMLResponse, summary="Student Career & Internship Portal")
def show_student_portal(request: Request):
    """Dedicated Student portal with job recommendations, application tracking, and bulletins"""
    student = _resolve_or_mock_user(request, required_role="Student")
    jobs = get_all_job_posting_records(active_only=True)
    all_applications = get_all_application_records()
    student_apps = [a for a in all_applications if a.user_id == student.id]
    announcements = get_all_announcement_records()

    return HTMLResponse(
        content=render_student_portal(
            student=student,
            jobs=jobs,
            applications=student_apps,
            announcements=announcements
        )
    )


# ---------------------------------------------------------
# 2. Alumni Portal (GET /portal/alumni)
# ---------------------------------------------------------
@portal_router.get("/portal/alumni", response_class=HTMLResponse, summary="Alumni Solidarity & Mentorship Portal")
def show_alumni_portal(request: Request):
    """Dedicated Alumni portal for community networking, job referrals, and mentorship"""
    alumni = _resolve_or_mock_user(request, required_role="Alumni")
    all_jobs = get_all_job_posting_records()
    all_users = get_all_user_records()
    all_alumni = [u for u in all_users if u.role == "Alumni"]
    announcements = get_all_announcement_records()

    return HTMLResponse(
        content=render_alumni_portal(
            alumni=alumni,
            alumni_jobs=all_jobs,
            all_alumni=all_alumni,
            announcements=announcements
        )
    )


# ---------------------------------------------------------
# 3. Recruiter Portal (GET /portal/recruiter)
# ---------------------------------------------------------
@portal_router.get("/portal/recruiter", response_class=HTMLResponse, summary="Corporate Recruiter & Talent Portal")
def show_recruiter_portal(request: Request):
    """Dedicated Recruiter portal for corporate job management and applicant review"""
    recruiter = _resolve_or_mock_user(request, required_role="Recruiter")
    jobs = get_all_job_posting_records()
    applications = get_all_application_records()
    talent_pool = [u for u in get_all_user_records() if u.role in ("Student", "Alumni")]

    return HTMLResponse(
        content=render_recruiter_portal(
            recruiter=recruiter,
            posted_jobs=jobs,
            applications=applications,
            talent_pool=talent_pool
        )
    )


# ---------------------------------------------------------
# 4. Academic Portal (GET /portal/academic)
# ---------------------------------------------------------
@portal_router.get("/portal/academic", response_class=HTMLResponse, summary="Academic Faculty & Departmental Portal")
def show_academic_portal(request: Request):
    """Dedicated Academic portal for faculty notices and departmental student directory"""
    academic = _resolve_or_mock_user(request, required_role="Academic")
    department_users = [u for u in get_all_user_records() if u.role in ("Student", "Alumni")]
    announcements = get_all_announcement_records()

    return HTMLResponse(
        content=render_academic_portal(
            academic=academic,
            department_users=department_users,
            announcements=announcements
        )
    )
