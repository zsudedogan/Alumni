"""
ApiJobPostingController - MVC Architecture
Handles Direct REST API routes (/api/job-postings) and Nested routes (/api/users/{user_id}/job-postings).
Provides complete CRUD endpoints, relationship resolution, and parameter validation.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from models.user import UserModel
from models.job_posting import (
    JobPosting,
    JobPostingCreate,
    JobPostingUpdate,
    JobPostingPatch,
    JobPostingWithUser,
    JobPostingModel,
)

# ---------------------------------------------------------
# Routers: Direct and Nested Routers
# ---------------------------------------------------------
DIRECT_TAG = "ApiJobPostingController (/api/job-postings)"
NESTED_TAG = "Nested Routes: Users -> JobPostings (/api/users/{user_id}/job-postings)"

api_job_posting_router = APIRouter(prefix="/api/job-postings", tags=[DIRECT_TAG])
nested_job_posting_router = APIRouter(prefix="/api/users/{user_id}/job-postings", tags=[NESTED_TAG])


# ---------------------------------------------------------
# Controller Class
# ---------------------------------------------------------
class ApiJobPostingController:
    """Controller implementing CRUD operations for Job Postings and nested user relationships"""

    # --- Direct Operations ---
    @staticmethod
    def list_all(active_only: bool = False, user_id: Optional[int] = None) -> List[JobPosting]:
        """CRUD: List all job postings, optionally filtered"""
        return JobPostingModel.get_all(active_only=active_only, user_id=user_id)

    @staticmethod
    def get_by_id(job_id: int) -> JobPostingWithUser:
        """CRUD: Get single job posting by ID including related user data"""
        job = JobPostingModel.get_with_user(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )
        return job

    @staticmethod
    def create(data: JobPostingCreate) -> JobPosting:
        """CRUD: Create a new job posting directly"""
        if data.user_id is not None:
            user = UserModel.get_by_id(data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {data.user_id} was not found"
                )
        return JobPostingModel.create(data)

    @staticmethod
    def update(job_id: int, data: JobPostingUpdate) -> JobPosting:
        """CRUD: Full update of job posting"""
        if data.user_id is not None:
            user = UserModel.get_by_id(data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {data.user_id} was not found"
                )
        updated = JobPostingModel.update(job_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )
        return updated

    @staticmethod
    def patch(job_id: int, data: JobPostingPatch) -> JobPosting:
        """CRUD: Partial update of job posting"""
        if data.user_id is not None:
            user = UserModel.get_by_id(data.user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {data.user_id} was not found"
                )
        patched = JobPostingModel.patch(job_id, data)
        if not patched:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )
        return patched

    @staticmethod
    def delete(job_id: int) -> dict:
        """CRUD: Delete job posting by ID"""
        deleted = JobPostingModel.delete(job_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} was not found"
            )
        return {
            "message": f"Job posting with ID {job_id} has been successfully deleted",
            "deleted_job_posting": deleted
        }

    # --- Nested Operations (Users -> JobPostings) ---
    @staticmethod
    def list_user_jobs(user_id: int) -> List[JobPosting]:
        """Nested: List all job postings belonging to a specific user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        return JobPostingModel.get_all(user_id=user_id)

    @staticmethod
    def create_user_job(user_id: int, data: JobPostingCreate) -> JobPosting:
        """Nested: Create a new job posting assigned specifically to user_id"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        # Ensure user_id is set to path parameter
        data.user_id = user_id
        return JobPostingModel.create(data)

    @staticmethod
    def get_user_job_by_id(user_id: int, job_id: int) -> JobPostingWithUser:
        """Nested: Retrieve a specific job posting under a specific user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        job = JobPostingModel.get_with_user(job_id)
        if not job or job.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} belonging to user {user_id} was not found"
            )
        return job

    @staticmethod
    def delete_user_job(user_id: int, job_id: int) -> dict:
        """Nested: Delete a specific job posting under a specific user"""
        user = UserModel.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} was not found"
            )
        job = JobPostingModel.get_by_id(job_id)
        if not job or job.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job posting with ID {job_id} belonging to user {user_id} was not found"
            )
        JobPostingModel.delete(job_id)
        return {
            "message": f"Job posting with ID {job_id} under user {user_id} has been successfully deleted"
        }


# =========================================================
# 1. DIRECT ROUTES (/api/job-postings)
# =========================================================

# GET /api/job-postings and /
@api_job_posting_router.get("", response_model=List[JobPosting], summary="List all job postings (Direct)")
@api_job_posting_router.get("/", response_model=List[JobPosting], include_in_schema=False)
async def get_all_job_postings(
    active_only: bool = Query(False, description="Filter only active job postings"),
    user_id: Optional[int] = Query(None, description="Filter by publisher user ID")
):
    """Retrieve all job postings via direct route"""
    return ApiJobPostingController.list_all(active_only=active_only, user_id=user_id)


# GET /api/job-postings/{id}
@api_job_posting_router.get("/{id}", response_model=JobPostingWithUser, summary="Get job posting by ID with user info (Direct)")
async def get_single_job_posting(id: int):
    """Retrieve single job posting with recruiter information"""
    return ApiJobPostingController.get_by_id(id)


# POST /api/job-postings and /
@api_job_posting_router.post("", response_model=JobPosting, status_code=status.HTTP_201_CREATED, summary="Create job posting (Direct)")
@api_job_posting_router.post("/", response_model=JobPosting, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_job_posting(data: JobPostingCreate):
    """Create a new job posting directly"""
    return ApiJobPostingController.create(data)


# PUT /api/job-postings/{id}
@api_job_posting_router.put("/{id}", response_model=JobPosting, summary="Full update job posting (Direct)")
async def update_job_posting(id: int, data: JobPostingUpdate):
    """Replace all attributes of an existing job posting"""
    return ApiJobPostingController.update(id, data)


# PATCH /api/job-postings/{id}
@api_job_posting_router.patch("/{id}", response_model=JobPosting, summary="Partial update job posting (Direct)")
async def patch_job_posting(id: int, data: JobPostingPatch):
    """Partially update attributes of an existing job posting"""
    return ApiJobPostingController.patch(id, data)


# DELETE /api/job-postings/{id}
@api_job_posting_router.delete("/{id}", summary="Delete job posting (Direct)")
async def delete_job_posting(id: int):
    """Delete a job posting by ID"""
    return ApiJobPostingController.delete(id)


# =========================================================
# 2. NESTED ROUTES (/api/users/{user_id}/job-postings)
# =========================================================

# GET /api/users/{user_id}/job-postings
@nested_job_posting_router.get("", response_model=List[JobPosting], summary="List all job postings for a user (Nested)")
@nested_job_posting_router.get("/", response_model=List[JobPosting], include_in_schema=False)
async def get_user_job_postings(user_id: int):
    """Retrieve all job postings created by a specific user (Nested resource)"""
    return ApiJobPostingController.list_user_jobs(user_id)


# POST /api/users/{user_id}/job-postings
@nested_job_posting_router.post("", response_model=JobPosting, status_code=status.HTTP_201_CREATED, summary="Create job posting under a user (Nested)")
@nested_job_posting_router.post("/", response_model=JobPosting, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_job_posting_for_user(user_id: int, data: JobPostingCreate):
    """Create a new job posting associated with a specific user (Nested resource)"""
    return ApiJobPostingController.create_user_job(user_id, data)


# GET /api/users/{user_id}/job-postings/{job_id}
@nested_job_posting_router.get("/{job_id}", response_model=JobPostingWithUser, summary="Get a user's specific job posting (Nested)")
async def get_specific_user_job(user_id: int, job_id: int):
    """Retrieve a specific job posting that belongs to a specific user"""
    return ApiJobPostingController.get_user_job_by_id(user_id, job_id)


# DELETE /api/users/{user_id}/job-postings/{job_id}
@nested_job_posting_router.delete("/{job_id}", summary="Delete a user's specific job posting (Nested)")
async def delete_specific_user_job(user_id: int, job_id: int):
    """Delete a specific job posting that belongs to a specific user"""
    return ApiJobPostingController.delete_user_job(user_id, job_id)
