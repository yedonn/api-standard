from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class Error(BaseModel):
    code: int  # Utiliser des entiers pour les codes d'état HTTP
    message: str
    details: Optional[Any] = None
    trace_id: Optional[str] = None
    timestamp: Optional[str] = None

class ErrorResponse(BaseModel):
    status: str = "error"
    error: Error

class Pagination(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    items_per_page: int

class SuccessResponse(BaseModel):
    status: str = "success"
    message: str
    data: Optional[Any] = None
    pagination: Optional[Pagination] = None