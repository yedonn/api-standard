from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.auth import get_hashed_password
from app.schemas.user import UserCreate, UserRead,UserUpdate
from app.api.v1.dependencies import get_user_service, UserService
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def create_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
):
    # Hash le mot de passe en accédant à l'attribut directement
    hashed_password = get_hashed_password(user.password)
    
    # Créer une nouvelle instance de UserCreate avec le mot de passe hashé
    user.password = hashed_password
    
    # Passer l'objet modifié au service
    created_user = await service.create_user(user)
    
    if created_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return created_user

# Read user by ID
@router.get("/{user_id}", response_model=UserRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    try:
        user = await service.get_user_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message": "User not found", "status": status.HTTP_404_NOT_FOUND})
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update user by ID
@router.put("/{user_id}", response_model=UserRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_user(
    user_id: int,
    user: UserUpdate,
    service: UserService = Depends(get_user_service)
):
        updated_user = await service.update_user(user_id, user)
        if updated_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"User not found","status":status.HTTP_404_NOT_FOUND})
        return updated_user

# Delete user by ID
@router.delete("/{user_id}", response_model=UserRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
        deleted_user = await service.delete_user(user_id)
        if deleted_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"User not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_user

# Get all users with pagination
@router.get("", response_model=List[UserRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_users(
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    deleted: Optional[bool] = False,
    service: UserService = Depends(get_user_service)
):
    return await service.get_users(skip=skip, limit=limit, deleted=deleted,order_by=sort)
        

# Filter users with optional parameters
@router.get("/search", response_model=List[UserRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_users(
    filters: Optional[Dict[str, str]] = None,  # Changement ici
    skip: int = 0,
    limit: int = 10,
    sort: str = 'id',
    service: UserService = Depends(get_user_service)
):
    filters = filters or {}  # Assurez-vous qu'il est initialisé en dict
    return await service.filter_users(filters=filters, skip=skip, limit=limit, order_by=sort)