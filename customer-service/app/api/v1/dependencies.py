from fastapi import Depends

from app.domain.services.session_service import SessionService
from app.domain.services.device_service import DeviceService
from app.domain.services.user_service import UserService
from app.domain.services.otp_service import OtpService

from app.db.repositories.repository import SessionRepository, DeviceRepository, UserRepository, OtpRepository

from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Dans certains cas, vous pourriez vouloir faire appel à une fonction
# ou une factory pour créer le service, et donc vous pourriez avoir :
def get_user_service(session: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(session)
    return UserService(user_repository)

def get_session_service(session: AsyncSession = Depends(get_db)):
    session_repository = SessionRepository(session)
    return SessionService(session_repository)

def get_device_service(session: AsyncSession = Depends(get_db)):
    device_repository = DeviceRepository(session)
    return DeviceService(device_repository)

def get_otp_service(session: AsyncSession = Depends(get_db)):
    otp_repository = OtpRepository(session)
    return OtpService(otp_repository)