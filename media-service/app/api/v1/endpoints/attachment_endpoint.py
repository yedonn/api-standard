from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.attachment import AttachmentCreate, AttachmentRead, AttachmentUpdate
from app.api.v1.dependencies import get_attachment_service, AttachmentService
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("", response_model=AttachmentRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_attachment(
    attachment: AttachmentCreate,
    service: AttachmentService = Depends(get_attachment_service)
):
    # Passer l'objet modifié au service
    created_attachment = await service.create_attachment(attachment)
    
    if created_attachment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    
    return created_attachment

# Read attachment by ID
@router.get("/{attachment_id}", response_model=AttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_attachment(
    attachment_id: int,
    service: AttachmentService = Depends(get_attachment_service)
):
    try:
        attachment = await service.get_attachment_by_id(attachment_id)
        if attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Attachment not found", "status": status.HTTP_404_NOT_FOUND})
        return attachment
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update attachment by ID
@router.put("/{attachment_id}", response_model=AttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_attachment(
    attachment_id: int,
    attachment: AttachmentUpdate,
    service: AttachmentService = Depends(get_attachment_service)
):
        updated_attachment = await service.update_attachment(attachment_id, attachment)
        if updated_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Attachment not found","status":status.HTTP_404_NOT_FOUND})
        return updated_attachment

# Soft Delete attachment by ID
@router.delete("/{attachment_id}/soft_delete", response_model=AttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_attachment(
    attachment_id: int,
    service: AttachmentService = Depends(get_attachment_service)
):
        deleted_attachment = await service.soft_delete_attachment(attachment_id)
        if deleted_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Attachment not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_attachment

# Delete attachment by ID
@router.delete("/{attachment_id}", response_model=AttachmentRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_attachment(
    attachment_id: int,
    service: AttachmentService = Depends(get_attachment_service)
):
        deleted_attachment = await service.delete_attachment(attachment_id)
        if deleted_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Attachment not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_attachment

# Get all attachments with pagination
@router.get("", response_model=List[AttachmentRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_attachments(
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    deleted: Optional[bool] = False,
    service: AttachmentService = Depends(get_attachment_service)
):
    return await service.get_attachments(skip=skip, limit=limit, deleted=deleted,order_by=sort)
        

# Filter attachments with optional parameters
@router.get("/search", response_model=List[AttachmentRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_attachments(
    filters: Optional[Dict[str, str]] = None,  # Changement ici
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    service: AttachmentService = Depends(get_attachment_service)
):
    filters = filters or {}  # Assurez-vous qu'il est initialisé en dict
    return await service.filter_attachments(filters=filters, skip=skip, limit=limit, order_by=sort)