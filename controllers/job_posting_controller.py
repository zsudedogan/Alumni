"""
JobPostingController - MVC Architecture
Controller handling Job Posting web routes (/job-postings and /job-postings/) with View Layer.
Provides HTML management interface, listing, and web form submissions.
"""

from typing import Optional
from fastapi import APIRouter, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse
from models.job_posting import JobPostingCreate, JobPostingModel
from models.user import UserModel
from views.job_posting_view import render_job_posting_management_page

TAG = "JobPostingController (/job-postings)"

job_posting_router = APIRouter(prefix="/job-postings", tags=[TAG])


class JobPostingController:
    """Standard Job Posting Web Controller connecting Model to View Layer"""

    @staticmethod
    def render_interface() -> HTMLResponse:
        """CRUD (Read - R): Render HTML View Layer management page"""
        jobs = JobPostingModel.get_all()
        users = UserModel.get_all()
        html = render_job_posting_management_page(jobs, available_users=users)
        return HTMLResponse(content=html)

    @staticmethod
    def handle_form_create(
        title: str,
        company: str,
        location: Optional[str] = "Remote",
        job_type: Optional[str] = "Full-time",
        description: str = "",
        requirements: Optional[str] = None,
        salary_range: Optional[str] = None,
        application_deadline: Optional[str] = None,
        contact_email: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> RedirectResponse:
        """CRUD (Create - C): Create job posting from web form and redirect"""
        payload = JobPostingCreate(
            title=title,
            company=company,
            location=location or "Remote",
            job_type=job_type or "Full-time",
            description=description,
            requirements=requirements or None,
            salary_range=salary_range or None,
            application_deadline=application_deadline or None,
            contact_email=contact_email or None,
            user_id=user_id or None,
        )
        JobPostingModel.create(payload)
        return RedirectResponse(url="/job-postings/", status_code=status.HTTP_303_SEE_OTHER)


# ---------------------------------------------------------
# Web Routes
# ---------------------------------------------------------
@job_posting_router.get("", response_class=HTMLResponse, summary="Open Job Postings Management Interface (View Layer)")
@job_posting_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def view_job_postings():
    """Renders the HTML interface for managing job postings"""
    return JobPostingController.render_interface()


@job_posting_router.post("", response_class=RedirectResponse, summary="Publish job posting via Web Form (View Layer)")
@job_posting_router.post("/", response_class=RedirectResponse, include_in_schema=False)
async def create_job_posting_from_form(
    title: str = Form(...),
    company: str = Form(...),
    location: Optional[str] = Form("Remote"),
    job_type: Optional[str] = Form("Full-time"),
    description: str = Form(...),
    requirements: Optional[str] = Form(None),
    salary_range: Optional[str] = Form(None),
    application_deadline: Optional[str] = Form(None),
    contact_email: Optional[str] = Form(None),
    user_id: Optional[int] = Form(None),
):
    """Handles HTML form submission for creating a new job posting"""
    return JobPostingController.handle_form_create(
        title=title,
        company=company,
        location=location,
        job_type=job_type,
        description=description,
        requirements=requirements,
        salary_range=salary_range,
        application_deadline=application_deadline,
        contact_email=contact_email,
        user_id=user_id,
    )
