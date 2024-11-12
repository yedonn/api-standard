from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.type_attachment import TypeAttachmentCreate, TypeAttachmentRead,TypeAttachmentUpdate
from app.api.v1.dependencies import get_type_attachment_service, TypeAttachmentService
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("", response_model=TypeAttachmentRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_type_attachment(
    type_attachment: TypeAttachmentCreate,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
    # Passer l'objet modifié au service
    created_type_attachment = await service.create_type_attachment(type_attachment)
    
    if created_type_attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
    
    return created_type_attachment

# Read type_attachment by ID
@router.get("/{type_attachment_id}", response_model=TypeAttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_type_attachment(
    type_attachment_id: int,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
    try:
        type_attachment = await service.get_type_attachment_by_id(type_attachment_id)
        if type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "TypeAttachment not found", "status": status.HTTP_404_NOT_FOUND})
        return type_attachment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update type_attachment by ID
@router.put("/{type_attachment_id}", response_model=TypeAttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_type_attachment(
    type_attachment_id: int,
    type_attachment: TypeAttachmentUpdate,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
        updated_type_attachment = await service.update_type_attachment(type_attachment_id, type_attachment)
        if updated_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"TypeAttachment not found","status":status.HTTP_404_NOT_FOUND})
        return updated_type_attachment


# Soft Delete type_attachment by ID
@router.delete("/{type_attachment_id}/soft_delete", response_model=TypeAttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def soft_delete_type_attachment(
    type_attachment_id: int,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
        deleted_type_attachment = await service.soft_delete_type_attachment(type_attachment_id)
        if deleted_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"TypeAttachment not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_type_attachment

# Delete type_attachment by ID
@router.delete("/{type_attachment_id}", response_model=TypeAttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_type_attachment(
    type_attachment_id: int,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
        deleted_type_attachment = await service.delete_type_attachment(type_attachment_id)
        if deleted_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"TypeAttachment not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_type_attachment

# Get all type_attachments with pagination
@router.get("", response_model=List[TypeAttachmentRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_type_attachments(
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    deleted: Optional[bool] = False,
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
    total_items, items = await service.get_type_attachments(skip=skip, limit=limit, deleted=deleted,order_by=sort)
    total_pages = (total_items + limit - 1) // limit  # Calculate total pages

    return items
        

# Filter type_attachments with optional parameters
@router.get("/search", response_model=List[TypeAttachmentRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_type_attachments(
    filters: Optional[Dict[str, str]] = None,  # Changement ici
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    service: TypeAttachmentService = Depends(get_type_attachment_service)
):
    filters = filters or {}  # Assurez-vous qu'il est initialisé en dict
    total_items, items = await service.filter_type_attachments(filters=filters, skip=skip, limit=limit, order_by=sort)
    total_pages = (total_items + limit - 1) // limit  # Calculate total pages

    return items