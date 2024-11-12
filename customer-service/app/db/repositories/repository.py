from sqlalchemy.ext.asyncio import AsyncSession
from app.db.index_model import DeviceModel, OtpModel, SessionModel, UserModel, UserInfoModel
from app.db.repositories.base import BaseRepository

class DeviceRepository(BaseRepository[DeviceModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(DeviceModel, db)

class OtpRepository(BaseRepository[OtpModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(OtpModel, db)

class SessionRepository(BaseRepository[SessionModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(SessionModel, db)

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserModel, db)

class UserInfoRepository(BaseRepository[UserInfoModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(UserInfoModel, db)