"""
Admin Controller - MVC Architecture
Provides comprehensive CRUD data manipulation and management dashboard for System Administrators.
Protected by AuthMiddleware: only users with role='Admin' can access these routes.
"""

from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Request, Form, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from models.user import (
    get_all_user_records,
    get_user_record_by_id,
    patch_user_record,
    delete_user_record,
    create_user_record,
    UserCreate,
    UserPatch,
)
from models.announcement import (
    get_all_announcement_records,
    create_announcement_record,
    delete_announcement_record,
    AnnouncementCreate,
)
from models.job_posting import (
    get_all_job_posting_records,
    get_job_posting_record_by_id,
    patch_job_posting_record,
    delete_job_posting_record,
    JobPostingPatch,
)
from models.application import (
    get_all_application_records,
    get_application_record_by_id,
    patch_application_record,
    delete_application_record,
    ApplicationPatch,
)
from views.admin_view import render_admin_dashboard

admin_router = APIRouter(tags=["Admin Panel & Data Manipulation"])


# ---------------------------------------------------------
# Web View: Admin Dashboard
# ---------------------------------------------------------

@admin_router.get("/admin/", response_class=HTMLResponse, summary="Admin Dashboard (View Layer)")
def show_admin_panel(
    request: Request,
    msg: Optional[str] = Query(None),
    err: Optional[str] = Query(None)
):
    """
    Renders the unified UniBridge Admin Control Dashboard.
    Requires role='Admin' (enforced by AuthMiddleware).
    """
    current_user = getattr(request.state, "user", None)
    users = get_all_user_records()
    announcements = get_all_announcement_records()
    jobs = get_all_job_posting_records()
    applications = get_all_application_records()

    return HTMLResponse(
        content=render_admin_dashboard(
            current_user=current_user,
            users=users,
            announcements=announcements,
            jobs=jobs,
            applications=applications,
            message=msg,
            error=err
        )
    )


@admin_router.get("/admin", response_class=HTMLResponse, include_in_schema=False)
def show_admin_panel_no_slash(
    request: Request,
    msg: Optional[str] = Query(None),
    err: Optional[str] = Query(None)
):
    """Fallback without trailing slash"""
    return show_admin_panel(request, msg=msg, err=err)


# ---------------------------------------------------------
# User Data Manipulation Endpoints
# ---------------------------------------------------------

@admin_router.post("/admin/users/{user_id}/role", summary="Change User Role")
def admin_change_user_role(user_id: int, role: str = Form(...)):
    """Allows Admin to reassign any user's role (Admin, Student, Alumni, Academic, Recruiter)"""
    patch_data = UserPatch(role=role)
    updated = patch_user_record(user_id, patch_data)
    if not updated:
        return RedirectResponse(url="/admin/?err=User+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=User+{user_id}+role+changed+to+{role}", status_code=303)


@admin_router.post("/admin/users/{user_id}/edit", summary="Edit User Details")
def admin_edit_user(
    user_id: int,
    name: str = Form(...),
    email: str = Form(...),
    department: Optional[str] = Form(None),
    role: str = Form(...)
):
    """Allows Admin to update profile details of a user"""
    patch_data = UserPatch(name=name, email=email, department=department, role=role)
    updated = patch_user_record(user_id, patch_data)
    if not updated:
        return RedirectResponse(url="/admin/?err=User+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=User+{name}+updated+successfully", status_code=303)


@admin_router.post("/admin/users/{user_id}/delete", summary="Delete User Record")
def admin_delete_user(request: Request, user_id: int):
    """Allows Admin to delete a user record"""
    current_user = getattr(request.state, "user", None)
    if current_user and current_user.id == user_id:
        return RedirectResponse(url="/admin/?err=Admin+cannot+delete+their+own+account", status_code=303)

    deleted = delete_user_record(user_id)
    if not deleted:
        return RedirectResponse(url="/admin/?err=User+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=User+{deleted.name}+deleted+successfully", status_code=303)


@admin_router.post("/admin/users/create", summary="Create User from Admin Panel")
def admin_create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form("password123"),
    role: str = Form("Student"),
    department: Optional[str] = Form(None)
):
    """Allows Admin to directly register a user"""
    new_user = UserCreate(
        name=name,
        email=email,
        password=password,
        role=role,
        department=department
    )
    created = create_user_record(new_user)
    return RedirectResponse(url=f"/admin/?msg=User+{created.name}+created+successfully", status_code=303)


# ---------------------------------------------------------
# Announcement Manipulation Endpoints
# ---------------------------------------------------------

@admin_router.post("/admin/announcements/create", summary="Publish Announcement")
def admin_create_announcement(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form("Genel")
):
    """Allows Admin to publish a new institutional announcement"""
    current_user = getattr(request.state, "user", None)
    author_name = current_user.name if current_user else "Admin"
    now_date = datetime.now().strftime("%Y-%m-%d")

    new_ann = AnnouncementCreate(
        title=title,
        content=content,
        category=category,
        author=author_name,
        date=now_date
    )
    created = create_announcement_record(new_ann)
    return RedirectResponse(url=f"/admin/?msg=Announcement+'{created.title}'+published+successfully", status_code=303)


@admin_router.post("/admin/announcements/{ann_id}/delete", summary="Delete Announcement")
def admin_delete_announcement(ann_id: int):
    """Allows Admin to delete an announcement"""
    deleted = delete_announcement_record(ann_id)
    if not deleted:
        return RedirectResponse(url="/admin/?err=Announcement+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=Announcement+deleted+successfully", status_code=303)


# ---------------------------------------------------------
# Job Posting Manipulation Endpoints
# ---------------------------------------------------------

@admin_router.post("/admin/jobs/{job_id}/toggle", summary="Toggle Job Posting Active Status")
def admin_toggle_job(job_id: int):
    """Allows Admin to toggle active/inactive status of a job posting"""
    job = get_job_posting_record_by_id(job_id)
    if not job:
        return RedirectResponse(url="/admin/?err=Job+not+found", status_code=303)

    new_status = not getattr(job, "is_active", True)
    patch_job_posting_record(job_id, JobPostingPatch(is_active=new_status))
    status_str = "Active" if new_status else "Inactive"
    return RedirectResponse(url=f"/admin/?msg=Job+{job_id}+marked+as+{status_str}", status_code=303)


@admin_router.post("/admin/jobs/{job_id}/delete", summary="Delete Job Posting")
def admin_delete_job(job_id: int):
    """Allows Admin to remove a job posting"""
    deleted = delete_job_posting_record(job_id)
    if not deleted:
        return RedirectResponse(url="/admin/?err=Job+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=Job+posting+deleted+successfully", status_code=303)


# ---------------------------------------------------------
# Application Manipulation Endpoints
# ---------------------------------------------------------

@admin_router.post("/admin/applications/{app_id}/status", summary="Update Application Status")
def admin_update_application_status(app_id: int, status: str = Form(...)):
    """Allows Admin to update application status (Pending, Reviewed, Accepted, Rejected)"""
    updated = patch_application_record(app_id, ApplicationPatch(status=status))
    if not updated:
        return RedirectResponse(url="/admin/?err=Application+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=Application+{app_id}+status+updated+to+{status}", status_code=303)


@admin_router.post("/admin/applications/{app_id}/delete", summary="Delete Application")
def admin_delete_application(app_id: int):
    """Allows Admin to delete an application"""
    deleted = delete_application_record(app_id)
    if not deleted:
        return RedirectResponse(url="/admin/?err=Application+not+found", status_code=303)
    return RedirectResponse(url=f"/admin/?msg=Application+deleted+successfully", status_code=303)


# ---------------------------------------------------------
# RESTful API Endpoints under /api/admin/...
# ---------------------------------------------------------

@admin_router.patch("/api/admin/users/{user_id}", summary="API: Update User (Admin)")
def api_admin_patch_user(user_id: int, patch_data: UserPatch):
    """Admin API to patch user details or role"""
    updated = patch_user_record(user_id, patch_data)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@admin_router.delete("/api/admin/users/{user_id}", summary="API: Delete User (Admin)")
def api_admin_delete_user(user_id: int):
    """Admin API to delete user"""
    deleted = delete_user_record(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted", "user": deleted}


@admin_router.delete("/api/admin/announcements/{ann_id}", summary="API: Delete Announcement (Admin)")
def api_admin_delete_announcement(ann_id: int):
    """Admin API to delete announcement"""
    deleted = delete_announcement_record(ann_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"message": "Announcement deleted", "announcement": deleted}
