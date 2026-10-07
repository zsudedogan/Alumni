"""
AnnouncementController - MVC Architecture
Controller dedicated to handling Announcement Web routes (/announcements/ and /announcements).
Connects to View layer to provide HTML Management Interface (Homework Requirement).
"""

from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import HTMLResponse
from models.announcement import (
    Announcement,
    AnnouncementCreate,
    AnnouncementUpdate,
    AnnouncementPatch,
    AnnouncementModel
)
from views.announcement_view import render_announcement_management_page

ANN_TAG = "AnnouncementController (/announcements)"

announcement_router = APIRouter(prefix="/announcements", tags=[ANN_TAG])


class AnnouncementController:
    """
    Standard Announcement Controller Class.
    Implements core application CRUD logic and connects to the View Layer.
    """

    # 1. READ ALL / VIEW INTERFACE (GET /announcements)
    @staticmethod
    def render_interface() -> HTMLResponse:
        """CRUD: Read all announcements and render HTML management interface (View Layer)"""
        announcements = AnnouncementModel.get_all()
        html = render_announcement_management_page(announcements)
        return HTMLResponse(content=html)

    @staticmethod
    def list_announcements() -> List[Announcement]:
        """CRUD: Read all announcements list"""
        return AnnouncementModel.get_all()

    # 2. READ BY ID (GET /announcements/{id})
    @staticmethod
    def get_announcement_by_id(ann_id: int) -> Announcement:
        """CRUD: Retrieve single announcement by ID"""
        ann = AnnouncementModel.get_by_id(ann_id)
        if not ann:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return ann

    # 3. CREATE (POST /announcements)
    @staticmethod
    def create_announcement(data: AnnouncementCreate) -> Announcement:
        """CRUD: Create announcement via AnnouncementModel"""
        return AnnouncementModel.create(data)

    # 4. UPDATE (PUT /announcements/{id})
    @staticmethod
    def update_announcement(ann_id: int, data: AnnouncementUpdate) -> Announcement:
        """CRUD: Full update of announcement by ID"""
        updated = AnnouncementModel.update(ann_id, data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return updated

    # 5. PATCH (PATCH /announcements/{id})
    @staticmethod
    def patch_announcement(ann_id: int, data: AnnouncementPatch) -> Announcement:
        """CRUD: Partial update of announcement by ID"""
        patched = AnnouncementModel.patch(ann_id, data)
        if not patched:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Announcement with ID {ann_id} was not found"
            )
        return patched

    # 6. DELETE (DELETE /announcements/{id})
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
            "message": f"Announcement with ID {ann_id} deleted successfully",
            "deleted_announcement": deleted
        }


# ---------------------------------------------------------
# Routes: Map /announcements and /announcements/ to AnnouncementController
# ---------------------------------------------------------

# GET /announcements and /announcements/ (Serves HTML View Layer Interface)
@announcement_router.get("", response_class=HTMLResponse, summary="Announcement Management Interface (View Layer) [AnnouncementController]")
@announcement_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def get_management_page():
    """Renders the HTML interface to manage announcements"""
    return AnnouncementController.render_interface()


# GET /announcements/data (JSON list for API/Client)
@announcement_router.get("/data", response_model=List[Announcement], summary="List announcements raw data [AnnouncementController]")
async def get_announcements_data():
    return AnnouncementController.list_announcements()


# GET /announcements/{id}
@announcement_router.get("/{id}", response_model=Announcement, summary="Get announcement by ID [AnnouncementController]")
async def get_single_announcement(id: int):
    return AnnouncementController.get_announcement_by_id(id)


# POST /announcements and /announcements/
@announcement_router.post("", response_model=Announcement, status_code=status.HTTP_201_CREATED, summary="Create announcement [AnnouncementController]")
@announcement_router.post("/", response_model=Announcement, status_code=status.HTTP_201_CREATED, include_in_schema=False)
async def create_new_announcement(data: AnnouncementCreate):
    return AnnouncementController.create_announcement(data)


# PUT /announcements/{id}
@announcement_router.put("/{id}", response_model=Announcement, summary="Full update announcement [AnnouncementController]")
async def update_existing_announcement(id: int, data: AnnouncementUpdate):
    return AnnouncementController.update_announcement(id, data)


# PATCH /announcements/{id}
@announcement_router.patch("/{id}", response_model=Announcement, summary="Partial update announcement [AnnouncementController]")
async def patch_existing_announcement(id: int, data: AnnouncementPatch):
    return AnnouncementController.patch_announcement(id, data)


# DELETE /announcements/{id}
@announcement_router.delete("/{id}", summary="Delete announcement [AnnouncementController]")
async def remove_announcement(id: int):
    return AnnouncementController.delete_announcement(id)
