from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.utilities.global_utils import create_error_response
from pydantic import ValidationError
from app.core.logging import log_message

# Gestion des erreurs de validation
async def validation_exception_handler(request: Request, exc: ValidationError):
    trace_id = getattr(request.state, 'trace_id', 'N/A')
    log_message(request=request,level="error", message=f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content= create_error_response(
            code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Erreur de validation des données",
            details=exc.errors(),  # Fournir les erreurs de validation
            trace_id=trace_id,  # Ajouter un identifiant de trace pour le débogage
        )
    )

# Gestion des erreurs HTTP spécifiques
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    trace_id = getattr(request.state, 'trace_id', 'N/A')
    log_message(request=request,level="error", message=f"HTTP error: {exc.detail}")

    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", "Erreur")
        data = exc.detail.get("data")
    else:
        message = exc.detail
        data = None
    
    return JSONResponse(
        status_code=exc.status_code,
        content=create_error_response(
            code=exc.status_code,
            message=message,
            details=data,
            trace_id=trace_id,  # Ajouter un identifiant de trace pour le débogage
        )
    )

# Gestion des erreurs génériques
async def generic_exception_handler(request: Request, exc: Exception):
    trace_id = getattr(request.state, 'trace_id', 'N/A')
    log_message(request=request,level="error", message=f"Unexpected error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_error_response(
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Une erreur interne est survenue.",
            details=str(exc),  # Inclure les détails de l'exception pour le débogage
            trace_id=trace_id,  # Ajouter un identifiant de trace pour le débogage
        )
    )
