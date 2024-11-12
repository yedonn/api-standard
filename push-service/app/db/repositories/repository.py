from sqlalchemy.ext.asyncio import AsyncSession
from app.db.index_model import NotificationModel, SubscriptionModel, ChannelModel, TypeNotificationModel, ScheduleModel, TemplateNotificationModel, AttachmentModel
from app.db.repositories.base import BaseRepository
    
class NotificationRepository(BaseRepository[NotificationModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(NotificationModel, db)

class SubscriptionRepository(BaseRepository[SubscriptionModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(SubscriptionModel, db)

class ChannelRepository(BaseRepository[ChannelModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ChannelModel, db)

class ScheduleRepository(BaseRepository[ScheduleModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(ScheduleModel, db)

class TypeNotificationRepository(BaseRepository[TypeNotificationModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(TypeNotificationModel, db)

class TemplateNotificationRepository(BaseRepository[TemplateNotificationModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(TemplateNotificationModel, db)

class AttachmentRepository(BaseRepository[AttachmentModel]):
    def __init__(self, db: AsyncSession):
        super().__init__(AttachmentModel, db)