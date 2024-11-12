from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
from app.api.v1.dependencies import get_notification_service, NotificationService
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("/immediate", response_model=NotificationRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_notification(
    notification: NotificationCreate,
    service: NotificationService = Depends(get_notification_service)
):
    # Passer l'objet modifié au service
    created_notification = await service.create_notification(notification)
    
    if created_notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    return created_notification

@router.post("/schedule", response_model=NotificationRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_notification(
    notification: NotificationCreate,
    service: NotificationService = Depends(get_notification_service)
):
    # Passer l'objet modifié au service
    created_notification = await service.create_notification(notification)
    
    if created_notification is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
    
    return created_notification

# Read notification by ID
@router.get("/{notification_id}", response_model=NotificationRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service)
):
    try:
        notification = await service.get_notification_by_id(notification_id)
        if notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Notification not found", "status": status.HTTP_404_NOT_FOUND})
        return notification
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update notification by ID
@router.put("/{notification_id}", response_model=NotificationRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_notification(
    notification_id: int,
    notification: NotificationUpdate,
    service: NotificationService = Depends(get_notification_service)
):
        updated_notification = await service.update_notification(notification_id, notification)
        if updated_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Notification not found","status":status.HTTP_404_NOT_FOUND})
        return updated_notification

# Delete notification by ID
@router.delete("/{notification_id}", response_model=NotificationRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_notification(
    notification_id: int,
    service: NotificationService = Depends(get_notification_service)
):
        deleted_notification = await service.delete_notification(notification_id)
        if deleted_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Notification not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_notification

# Get all notifications with pagination
@router.get("", response_model=List[NotificationRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_notifications(
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    deleted: Optional[bool] = False,
    service: NotificationService = Depends(get_notification_service)
):
    return await service.get_notifications(skip=skip, limit=limit, deleted=deleted,order_by=sort)
        

# Filter notifications with optional parameters
@router.get("/search", response_model=List[NotificationRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_notifications(
    filters: Optional[Dict[str, str]] = None,  # Changement ici
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    service: NotificationService = Depends(get_notification_service)
):
    filters = filters or {}  # Assurez-vous qu'il est initialisé en dict
    return await service.filter_notifications(filters=filters, skip=skip, limit=limit, order_by=sort)