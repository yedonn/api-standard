
from fastapi import APIRouter

from app.api.v1.endpoints import attachment_endpoint, type_attachment_endpoint

from app.core.config import settings

router = APIRouter()
version="/v1"
app_name=settings.APPNAME

router.include_router(attachment_endpoint.router, prefix=f"{version}/attachments",
                      tags=[f"{app_name} - Attachments"])
router.include_router(type_attachment_endpoint.router, prefix=f"{version}/type_attachments",
                      tags=[f"{app_name} - Type Attachments"])