from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead,SubscriptionUpdate
from app.api.v1.dependencies import get_subscription_service, SubscriptionService
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("", response_model=SubscriptionRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_subscription(
    subscription: SubscriptionCreate,
    service: SubscriptionService = Depends(get_subscription_service)
):
    # Passer l'objet modifié au service
    created_subscription = await service.create_subscription(subscription)
    
    if created_subscription is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    
    return created_subscription

# Read subscription by ID
@router.get("/{subscription_id}", response_model=SubscriptionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_subscription(
    subscription_id: int,
    service: SubscriptionService = Depends(get_subscription_service)
):
    try:
        subscription = await service.get_subscription_by_id(subscription_id)
        if subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "Subscription not found", "status": status.HTTP_404_NOT_FOUND})
        return subscription
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update subscription by ID
@router.put("/{subscription_id}", response_model=SubscriptionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_subscription(
    subscription_id: int,
    subscription: SubscriptionUpdate,
    service: SubscriptionService = Depends(get_subscription_service)
):
        updated_subscription = await service.update_subscription(subscription_id, subscription)
        if updated_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Subscription not found","status":status.HTTP_404_NOT_FOUND})
        return updated_subscription

# Delete subscription by ID
@router.delete("/{subscription_id}", response_model=SubscriptionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_subscription(
    subscription_id: int,
    service: SubscriptionService = Depends(get_subscription_service)
):
        deleted_subscription = await service.delete_subscription(subscription_id)
        if deleted_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Subscription not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_subscription

# Get all subscriptions with pagination
@router.get("", response_model=List[SubscriptionRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_subscriptions(
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    deleted: Optional[bool] = False,
    service: SubscriptionService = Depends(get_subscription_service)
):
    return await service.get_subscriptions(skip=skip, limit=limit, deleted=deleted,order_by=sort)
        

# Filter subscriptions with optional parameters
@router.get("/search", response_model=List[SubscriptionRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_subscriptions(
    filters: Optional[Dict[str, str]] = None,  # Changement ici
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    service: SubscriptionService = Depends(get_subscription_service)
):
    filters = filters or {}  # Assurez-vous qu'il est initialisé en dict
    return await service.filter_subscriptions(filters=filters, skip=skip, limit=limit, order_by=sort)