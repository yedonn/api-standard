from fastapi import HTTPException, Request
from app.schemas.api_response import Error, SuccessResponse, ErrorResponse, Pagination
from app.utilities.consul_utils import get_service_url
from datetime import datetime
from typing import Any, Optional
import requests

def create_success_response(message: str, data: Any = None, pagination: Optional[Pagination] = None) -> SuccessResponse:
    return SuccessResponse(
        message=message,
        data=data,
        pagination=pagination
    ).dict()

def create_error_response(code: int, message: str, details: Optional[Any] = None, trace_id: Optional[str] = None) -> ErrorResponse:
    return ErrorResponse(
        error=Error(
            code=code,
            message=message,
            details=details,
            trace_id=trace_id,
            timestamp=datetime.utcnow().isoformat()  # Horodatage au format ISO 8601
        )
    ).dict()
    
def validate_token(request: Request, service_name: str):
    # Extrait le token JWT de l'en-tête Authorization
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token manquant")
    
    # Valide le token en le vérifiant via le User Service (via une requête HTTP)
    try:
        service_url = get_service_url(service_name)
        response = requests.get(f"{service_url}/api/v1/auth/verify-token", headers={"Authorization": token})
        # return response
        if response.status_code != 200:
            return response
            raise HTTPException(status_code=401, detail="Token invalide")
    except requests.RequestException:
        raise HTTPException(status_code=503, detail=f"Erreur avec le {service_name}")
    return response