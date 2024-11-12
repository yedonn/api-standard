import random
from app.schemas.api_response import Error, SuccessResponse, ErrorResponse, Pagination
from datetime import datetime
from typing import Any, Optional
import re

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
    
def is_email(texte):
    # Modèle d'expression régulière pour la validation d'une adresse e-mail
    modele_email = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'

    # Utilisation de re.match() pour vérifier si la chaîne correspond au modèle d'adresse e-mail
    if re.match(modele_email, texte):
        return True
    else:
        return False

def is_contact(phone_number):
    # Expression régulière pour vérifier le format du numéro de téléphone
    pattern = re.compile(r'^\+?[1-9]\d{1,14}$')

    # Vérifier si le numéro de téléphone correspond au format attendu
    if pattern.match(phone_number):
        return True
    else:
        return False
    
def generate_otp():
    """Génère un code OTP à 6 chiffres."""
    return str(random.randint(100000, 999999))