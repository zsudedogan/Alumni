"""
ApiAnnouncementController - MVC Architecture
Controller dedicated to handling REST API requests for Announcements (/api/announcements/ and /api/announcements).
Homework Requirement: One of 2 controllers for Announcement.
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from models.announcement import (
    Announcement,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementPatch,
    AnnouncementModel
)

API_ANN_TAG = "ApiAnnouncementController (/api/announcements)"

api_announcement_router = APIRouter(prefix="/api/announcements", tags=[API_ANN_TAG])


class ApiAnnouncementController:
    """
    API Announcement Controller Class.
    Implements CRUD operations for programmatic REST API client requests.
    """

    # 1. READ ALL (GET /api/announcements)
    @staticmethod
    def list_announcements() -> List[Announcement]:
        """CRUD: Read all announcements as JSON list"""
        return AnnouncementModel.get_all()

    # 2. READ BY ID (GET /api/announcements/{id})
    @staticmethod
    def get_announcement_by_id(ann_id: int) -> Announcement:
        """CRUD: Read single announcement by ID"""
        ann = AnnouncementModel.get_by_id(ann_id)
        if not ann:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return ann

    # 3. CREATE (POST /api/announcements)
    @staticmethod
    def create_announcement(data: AnnouncementCreate) -> Announcement:
        """CRUD: Create announcement via AnnouncementModel (Status 201 Created)"""
        return AnnouncementModel.create(data)

    # 4. UPDATE (PUT /api/announcements/{id})
    @staticmethod
    def update_announcement(ann_id: int, data: AnnouncementUpdate) -> Announcement:
        """CRUD: Full update of announcement attributes"""
        updated = AnnouncementModel.update(ann_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return updated

    # 5. PATCH (PATCH /api/announcements/{id})
    @staticmethod
    def patch_announcement(ann_id: int, data: AnnouncementPatch) -> Announcement:
        """CRUD: Partial update of announcement attributes"""
        patched = AnnouncementModel.patch(ann_id, data)
        if not patched:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return patched

    # 6. DELETE (DELETE /api/announcements/{id})
    @staticmethod
    def delete_announcement(ann_id: int) -> dict:
        """CRUD: Delete announcement by ID"""
        deleted = AnnouncementModel.delete(ann_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return {
            "message": f"Announcement with ID {ann_id} has been successfully deleted",
            "deleted_announcement": deleted
        }


# ---------------------------------------------------------
# Routes: Map /api/announcements and /api/announcements/ to ApiAnnouncementController
# ---------------------------------------------------------

@api_announcement_router.get("", response_model=List[Announcement], summary="List all announcements [ApiAnnouncementController]")
@api_announcement_router.get("/", response_model=List[Announcement], include_in_schema=False)
async def get_all_announcements():
    return ApiAnnouncementController.list_announcements()


@api_announcement_router.get("/{id}", response_model=Announcement, summary="Get announcement by ID [ApiAnnouncementController]")
async def get_single_announcement(id: int):
    return ApiAnnouncementController.get_announcement_by_id(id)


@api_announcement_router.post("", response_model=Announcement, status_code=status.HTTP_201_CREATED, summary="Create announcement [ApiAnnouncementController]")
@api_announcement_router.post("/", response_model=Announcement, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_announcement(data: AnnouncementCreate):
    return ApiAnnouncementController.create_announcement(data)


@api_announcement_router.put("/{id}", response_model=Announcement, summary="Full update announcement [ApiAnnouncementController]")
async def update_existing_announcement(id: int, data: AnnouncementUpdate):
    return ApiAnnouncementController.update_announcement(id, data)


@api_announcement_router.patch("/{id}", response_model=Announcement, summary="Partial update announcement [ApiAnnouncementController]")
async def patch_existing_announcement(id: int, data: AnnouncementPatch):
    return ApiAnnouncementController.patch_announcement(id, data)


@api_announcement_router.delete("/{id}", summary="Delete announcement [ApiAnnouncementController]")
async def remove_announcement(id: int):
    return ApiAnnouncementController.delete_announcement(id)
