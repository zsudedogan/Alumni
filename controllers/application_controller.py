"""
ApplicationController - MVC Architecture
Controller handling Application web routes (/applications and /applications/) with View Layer.
Provides HTML management interface, listing, and web form submissions.
"""

from typing import Optional
from fastapi import APIRouter, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from models.application import ApplicationCreate, ApplicationModel
from views.application_view import render_application_management_page

TAG = "ApplicationController (/applications)"

application_router = APIRouter(prefix="/applications", tags=[TAG])


class ApplicationController:
    """Standard Application Web Controller connecting Model to View Layer"""

    @staticmethod
    def render_interface() -> HTMLResponse:
        """CRUD (Read - R): Render HTML View Layer management page"""
        apps = ApplicationModel.get_all_with_details()
        html = render_application_management_page(apps)
        return HTMLResponse(content=html)

    @staticmethod
    def handle_form_create(
        job_id: int,
        user_id: int,
        resume_url: Optional[str] = None,
        cover_note: Optional[str] = None,
        status_val: Optional[str] = "Pending",
    ) -> RedirectResponse:
        """CRUD (Create - C): Create application from web form and redirect"""
        payload = ApplicationCreate(
            job_id=job_id,
            user_id=user_id,
            resume_url=resume_url or None,
            cover_note=cover_note or None,
            status=status_val or "Pending"
        )
        ApplicationModel.create(payload)
        return RedirectResponse(url="/applications/", status_code=status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------
# Web Routes
# ---------------------------------------------------------
@application_router.get("", response_class=HTMLResponse, summary="Open Applications Management Interface (View Layer)")
@application_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def view_applications():
    """Renders the HTML interface for managing job applications"""
    return ApplicationController.render_interface()


@application_router.post("", response_class=RedirectResponse, summary="Submit application via Web Form (View Layer)")
@application_router.post("/", response_class=RedirectResponse, include_in_schema=False)
async def create_application_from_form(
    job_id: int = Form(...),
    user_id: int = Form(...),
    resume_url: Optional[str] = Form(None),
    cover_note: Optional[str] = Form(None),
    status: Optional[str] = Form("Pending"),
):
    """Handles HTML form submission for creating a new job application"""
    return ApplicationController.handle_form_create(
        job_id=job_id,
        user_id=user_id,
        resume_url=resume_url,
        cover_note=cover_note,
        status_val=status
    )
