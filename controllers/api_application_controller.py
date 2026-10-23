"""
ApiApplicationController - MVC Architecture
Handles Direct REST API routes (/api/applications) and Nested routes:
- /api/job-postings/{job_id}/applications
- /api/users/{user_id}/applications
Provides complete CRUD endpoints, relationship resolution, and parameter validation.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from models.user import UserModel
from models.job_posting import JobPostingModel
from models.application import (
    Application,
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationPatch,
    ApplicationWithDetails,
    ApplicationModel,
)

# ---------------------------------------------------------
# Routers: Direct and Nested Routers
# ---------------------------------------------------------
DIRECT_TAG = "ApiApplicationController (/api/applications)"
JOB_NESTED_TAG = "Nested Routes: JobPostings -> Applications (/api/job-postings/{job_id}/applications)"
USER_NESTED_TAG = "Nested Routes: Users -> Applications (/api/users/{user_id}/applications)"

api_application_router = APIRouter(prefix="/api/applications", tags=[DIRECT_TAG])
nested_job_application_router = APIRouter(prefix="/api/job-postings/{job_id}/applications", tags=[JOB_NESTED_TAG])
nested_user_application_router = APIRouter(prefix="/api/users/{user_id}/applications", tags=[USER_NESTED_TAG])


# ---------------------------------------------------------
# Controller Class
# ---------------------------------------------------------
class ApiApplicationController:
    """Controller implementing CRUD operations for Applications and nested relationships"""

    # --- Direct Operations ---
    @staticmethod
    def list_all(
        job_id: Optional[int] = None,
        user_id: Optional[int] = None,
        status_filter: Optional[str] = None
    ) -> List[Application]:
        """CRUD: List all applications with optional query filters"""
        return ApplicationModel.get_all(job_id=job_id, user_id=user_id, status=status_filter)

    @staticmethod
    def get_by_id(app_id: int) -> ApplicationWithDetails:
        """CRUD: Get single application by ID with related applicant and job details"""
        app_record = ApplicationModel.get_with_details(app_id)
        if not app_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} was not found"
            )
        return app_record

    @staticmethod
    def create(data: ApplicationCreate) -> Application:
        """CRUD: Create a new application directly"""
        if not data.job_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Field 'job_id' is required"
            )
        if not data.user_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Field 'user_id' is required"
            )

        # Validate job existence
        job = JobPostingModel.get_by_id(data.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {data.job_id} was not found"
            )

        # Validate user existence
        user = UserModel.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {data.user_id} was not found"
            )

        return ApplicationModel.create(data)

    @staticmethod
    def update(app_id: int, data: ApplicationUpdate) -> Application:
        """CRUD: Full update of application"""
        # Validate job existence
        job = JobPostingModel.get_by_id(data.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {data.job_id} was not found"
            )

        # Validate user existence
        user = UserModel.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {data.user_id} was not found"
            )

        updated = ApplicationModel.update(app_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} was not found"
            )
        return updated

    @staticmethod
    def patch(app_id: int, data: ApplicationPatch) -> Application:
        """CRUD: Partial update of application"""
        if data.job_id is not None:
            job = JobPostingModel.get_by_id(data.job_id)
            if not job:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Job posting with ID {data.job_id} was not found"
                )

        if data.user_id is not None:
            user = UserModel.get_by_id(data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {data.user_id} was not found"
                )

        patched = ApplicationModel.patch(app_id, data)
        if not patched:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} was not found"
            )
        return patched

    @staticmethod
    def delete(app_id: int) -> dict:
        """CRUD: Delete application by ID"""
        deleted = ApplicationModel.delete(app_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {app_id} was not found"
            )
        return {
            "message": f"Application with ID {app_id} has been successfully deleted",
            "deleted_application": deleted
        }

    # --- Nested Operations: JobPostings -> Applications ---
    @staticmethod
    def list_job_applications(job_id: int) -> List[Application]:
        """Nested: List all applications for a specific job posting"""
        job = JobPostingModel.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )
        return ApplicationModel.get_all(job_id=job_id)

    @staticmethod
    def create_job_application(job_id: int, data: ApplicationCreate) -> Application:
        """Nested: Create an application for a specific job posting"""
        job = JobPostingModel.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )

        if not data.user_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Field 'user_id' is required"
            )

        user = UserModel.get_by_id(data.user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {data.user_id} was not found"
            )

        data.job_id = job_id
        return ApplicationModel.create(data)

    @staticmethod
    def get_job_application(job_id: int, application_id: int) -> ApplicationWithDetails:
        """Nested: Get specific application under a job posting"""
        job = JobPostingModel.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )

        app_record = ApplicationModel.get_with_details(application_id)
        if not app_record or app_record.job_id != job_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} for job {job_id} was not found"
            )
        return app_record

    @staticmethod
    def delete_job_application(job_id: int, application_id: int) -> dict:
        """Nested: Delete specific application under a job posting"""
        job = JobPostingModel.get_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )

        app_record = ApplicationModel.get_by_id(application_id)
        if not app_record or app_record.job_id != job_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} for job {job_id} was not found"
            )
        ApplicationModel.delete(application_id)
        return {
            "message": f"Application with ID {application_id} under job {job_id} has been successfully deleted"
        }

    # --- Nested Operations: Users -> Applications ---
    @staticmethod
    def list_user_applications(user_id: int) -> List[Application]:
        """Nested: List all applications submitted by a specific user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return ApplicationModel.get_all(user_id=user_id)

    @staticmethod
    def create_user_application(user_id: int, data: ApplicationCreate) -> Application:
        """Nested: Submit an application by a specific user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )

        if not data.job_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Field 'job_id' is required"
            )

        job = JobPostingModel.get_by_id(data.job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {data.job_id} was not found"
            )

        data.user_id = user_id
        return ApplicationModel.create(data)

    @staticmethod
    def get_user_application(user_id: int, application_id: int) -> ApplicationWithDetails:
        """Nested: Get specific application submitted by a user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )

        app_record = ApplicationModel.get_with_details(application_id)
        if not app_record or app_record.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} by user {user_id} was not found"
            )
        return app_record

    @staticmethod
    def delete_user_application(user_id: int, application_id: int) -> dict:
        """Nested: Delete specific application submitted by a user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )

        app_record = ApplicationModel.get_by_id(application_id)
        if not app_record or app_record.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with ID {application_id} by user {user_id} was not found"
            )
        ApplicationModel.delete(application_id)
        return {
            "message": f"Application with ID {application_id} by user {user_id} has been successfully deleted"
        }


# =========================================================
# 1. DIRECT ROUTES (/api/applications)
# =========================================================

# GET /api/applications and /
@api_application_router.get("", response_model=List[Application], summary="List all applications (Direct)")
@api_application_router.get("/", response_model=List[Application], include_in_schema=False)
async def get_all_applications(
    job_id: Optional[int] = Query(None, description="Filter by target Job ID"),
    user_id: Optional[int] = Query(None, description="Filter by applicant User ID"),
    status: Optional[str] = Query(None, description="Filter by status (Pending, Reviewed, Shortlisted, Accepted, Rejected)")
):
    """Retrieve all job applications via direct route with optional filtering"""
    return ApiApplicationController.list_all(job_id=job_id, user_id=user_id, status_filter=status)


# GET /api/applications/{id}
@api_application_router.get("/{id}", response_model=ApplicationWithDetails, summary="Get application by ID with details (Direct)")
async def get_single_application(id: int):
    """Retrieve single application with enriched applicant and job details"""
    return ApiApplicationController.get_by_id(id)


# POST /api/applications and /
@api_application_router.post("", response_model=Application, status_code=status.HTTP_201_CREATED, summary="Create application (Direct)")
@api_application_router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_application(data: ApplicationCreate):
    """Submit a new job application directly"""
    return ApiApplicationController.create(data)


# PUT /api/applications/{id}
@api_application_router.put("/{id}", response_model=Application, summary="Full update application (Direct)")
async def update_application(id: int, data: ApplicationUpdate):
    """Replace all attributes of an existing application"""
    return ApiApplicationController.update(id, data)


# PATCH /api/applications/{id}
@api_application_router.patch("/{id}", response_model=Application, summary="Partial update application (Direct)")
async def patch_application(id: int, data: ApplicationPatch):
    """Partially update status or note of an application"""
    return ApiApplicationController.patch(id, data)


# DELETE /api/applications/{id}
@api_application_router.delete("/{id}", summary="Delete application (Direct)")
async def delete_application(id: int):
    """Delete an application by ID"""
    return ApiApplicationController.delete(id)


# =========================================================
# 2. NESTED ROUTES: JobPostings -> Applications
# =========================================================

# GET /api/job-postings/{job_id}/applications
@nested_job_application_router.get("", response_model=List[Application], summary="List all applications for a job posting (Nested)")
@nested_job_application_router.get("/", response_model=List[Application], include_in_schema=False)
async def get_job_applications(job_id: int):
    """Retrieve all applications submitted for a specific job posting"""
    return ApiApplicationController.list_job_applications(job_id)


# POST /api/job-postings/{job_id}/applications
@nested_job_application_router.post("", response_model=Application, status_code=status.HTTP_201_CREATED, summary="Submit application to a job posting (Nested)")
@nested_job_application_router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def apply_to_job(job_id: int, data: ApplicationCreate):
    """Submit a new application for a specific job posting"""
    return ApiApplicationController.create_job_application(job_id, data)


# GET /api/job-postings/{job_id}/applications/{application_id}
@nested_job_application_router.get("/{application_id}", response_model=ApplicationWithDetails, summary="Get specific application for a job (Nested)")
async def get_specific_job_application(job_id: int, application_id: int):
    """Retrieve details of a specific application under a job posting"""
    return ApiApplicationController.get_job_application(job_id, application_id)


# DELETE /api/job-postings/{job_id}/applications/{application_id}
@nested_job_application_router.delete("/{application_id}", summary="Delete application from a job posting (Nested)")
async def delete_job_application_endpoint(job_id: int, application_id: int):
    """Delete an application submitted for a job posting"""
    return ApiApplicationController.delete_job_application(job_id, application_id)


# =========================================================
# 3. NESTED ROUTES: Users -> Applications
# =========================================================

# GET /api/users/{user_id}/applications
@nested_user_application_router.get("", response_model=List[Application], summary="List all applications submitted by a user (Nested)")
@nested_user_application_router.get("/", response_model=List[Application], include_in_schema=False)
async def get_user_applications(user_id: int):
    """Retrieve all applications submitted by a specific user"""
    return ApiApplicationController.list_user_applications(user_id)


# POST /api/users/{user_id}/applications
@nested_user_application_router.post("", response_model=Application, status_code=status.HTTP_201_CREATED, summary="Submit application by a user (Nested)")
@nested_user_application_router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def apply_as_user(user_id: int, data: ApplicationCreate):
    """Submit an application as a specific user"""
    return ApiApplicationController.create_user_application(user_id, data)


# GET /api/users/{user_id}/applications/{application_id}
@nested_user_application_router.get("/{application_id}", response_model=ApplicationWithDetails, summary="Get specific application submitted by user (Nested)")
async def get_specific_user_application(user_id: int, application_id: int):
    """Retrieve details of an application submitted by a specific user"""
    return ApiApplicationController.get_user_application(user_id, application_id)


# DELETE /api/users/{user_id}/applications/{application_id}
@nested_user_application_router.delete("/{application_id}", summary="Delete application submitted by user (Nested)")
async def delete_user_application_endpoint(user_id: int, application_id: int):
    """Delete an application submitted by a user"""
    return ApiApplicationController.delete_user_application(user_id, application_id)
