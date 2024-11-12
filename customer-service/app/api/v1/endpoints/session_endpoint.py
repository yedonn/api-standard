from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.schemas.session import SessionCreate, SessionRead,SessionUpdate
from app.domain.services.session_service import SessionService
from app.api.v1.dependencies import get_session_service
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

@router.post("/", response_model=SessionRead)
async def create_session(
    session: SessionCreate,
    service: SessionService = Depends(get_session_service)
):
    return await service.create_session(session)

# Read session by ID
@router.get("/{session_id}", response_model=SessionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_session(
    session_id: int,
    service: SessionService = Depends(get_session_service)
):
    try:
        session = await service.get_session_by_id(session_id)
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Session not found","status":status.HTTP_404_NOT_FOUND})
        return session
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_500_INTERNAL_SERVER_ERROR})

# Update session by ID
@router.put("/{session_id}", response_model=SessionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def update_session(
    session_id: int,
    session: SessionUpdate,
    service: SessionService = Depends(get_session_service)
):
    try:
        updated_session = await service.update_session(session_id, session)
        if updated_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Session not found","status":status.HTTP_404_NOT_FOUND})
        return updated_session
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_500_INTERNAL_SERVER_ERROR})

# Delete session by ID
@router.delete("/{session_id}", response_model=SessionRead, responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def delete_session(
    session_id: int,
    service: SessionService = Depends(get_session_service)
):
    try:
        deleted_session = await service.delete_session(session_id)
        if deleted_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"message":"Session not found","status":status.HTTP_404_NOT_FOUND})
        return deleted_session
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_404_NOT_FOUND})

# Get all sessions with pagination
@router.get("/", response_model=List[SessionRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_sessions(
    skip: int = 0,
    limit: int = 10,
    service: SessionService = Depends(get_session_service)
):
    try:
        return await service.get_sessions(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_404_NOT_FOUND})

# Get all sessions with pagination
@router.get("/all", response_model=List[SessionRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def get_sessions(
    skip: int = 0,
    limit: int = 10,
    service: SessionService = Depends(get_session_service)
):
    try:
        return await service.get_sessions(skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_404_NOT_FOUND})

# Filter sessions with optional parameters
@router.get("/filter", response_model=List[SessionRead], responses={status.HTTP_404_NOT_FOUND: {"model": ErrorResponse}, status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse}})
async def filter_sessions(
    user_id: Optional[int] = Query(None),
    is_active: Optional[bool] = Query(None),
    session: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 10,
    service: SessionService = Depends(get_session_service)
):
    try:
        return await service.filter_sessions(user_id=user_id, is_active=is_active, session=session, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"message":"Internal server error","status":status.HTTP_404_NOT_FOUND})