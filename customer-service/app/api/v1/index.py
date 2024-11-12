
from fastapi import APIRouter

from app.api.v1.endpoints import session_endpoint, user_endpoint, auth_endpoint

from app.core.config import settings

router = APIRouter()
version="/v1"
app_name=settings.APPNAME


router.include_router(auth_endpoint.router, prefix=f"{version}/auth",
                      tags=[f"{app_name} - Auth"])
router.include_router(session_endpoint.router, prefix=f"{version}/sessions",
                      tags=[f"{app_name} - Sessions"])
router.include_router(user_endpoint.router, prefix=f"{version}/users",
                      tags=[f"{app_name} - Users"])