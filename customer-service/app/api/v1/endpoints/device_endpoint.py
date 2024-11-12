from user_agents import parse
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from app.schemas.device import DeviceCreate, DeviceRead,DeviceUpdate
from app.domain.services.device_service import DeviceService
from app.api.v1.dependencies import get_device_service
from app.schemas.api_response import SuccessResponse, ErrorResponse
from app.utilities.global_utils import create_success_response, create_error_response

router = APIRouter()

# Fonction pour récupérer et créer/mise à jour des informations du périphérique
async def save_device_info(
    user_id: int,
    request: Request,
    device_service: DeviceService = Depends(get_device_service)
):
    user_agent = request.headers.get('user-agent')
    if not user_agent:
        raise HTTPException(status_code=400, detail={"message":"User-Agent header is missing or invalid", "statut": status.HTTP_400_BAD_REQUEST})
    parsed_agent = parse(user_agent)
    
    # Déterminer le type de périphérique
    device_type = "Mobile" if parsed_agent.is_mobile else "Tablet" if parsed_agent.is_tablet else "PC"
    device_os = parsed_agent.os.family
    device_name = parsed_agent.device.family

    # Tenter de récupérer un périphérique existant pour cet utilisateur
    devices = await device_service.filter_internal_devices({'user_id': user_id, 'device_name': device_name, 'device_os': device_os})
    
    if devices:
        # Si un périphérique est trouvé, on met à jour son dernier accès
        device = devices[0]  # On prend le premier correspondant
        device = await device_service.update_device(
            device.id,
            DeviceUpdate(last_accessed= datetime.utcnow(), is_active= True)
        )
    else:
        # Si aucun périphérique n'est trouvé, on en crée un nouveau
        device_data = DeviceCreate(
            device_type=device_type,
            device_os=device_os,
            device_name=device_name,
            user_id=user_id,  # Associer l'utilisateur au périphérique
            last_accessed=datetime.utcnow(),
            is_active=True
        )
        device = await device_service.create_device(device_data)

    return device