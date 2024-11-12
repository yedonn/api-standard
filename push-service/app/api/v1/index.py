
from fastapi import APIRouter

from app.api.v1.endpoints import notification_endpoint, subscription_endpoint

from app.core.config import settings

router = APIRouter()
version="/v1"
app_name=settings.APPNAME

router.include_router(notification_endpoint.router, prefix=f"{version}/notifications",
                      tags=[f"{app_name} - Notifications"])
router.include_router(subscription_endpoint.router, prefix=f"{version}/subscriptions",
                      tags=[f"{app_name} - Subscriptions"])