from fastapi import Depends

from app.domain.services.notification_service import NotificationService
from app.domain.services.subcription_service import SubscriptionService
from app.domain.services.channel_service import ChannelService
from app.domain.services.attachment_service import AttachmentService
from app.domain.services.template_notification_service import TemplateNotificationService
from app.domain.services.type_notification_service import TypeNotificationService
from app.domain.services.schedule_service import ScheduleService

from app.db.repositories.repository import NotificationRepository, SubscriptionRepository, ScheduleRepository, ChannelRepository, AttachmentRepository, TemplateNotificationRepository, TypeNotificationRepository

from app.db.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

# Dans certains cas, vous pourriez vouloir faire appel à une fonction
# ou une factory pour créer le service, et donc vous pourriez avoir :
def get_notification_service(session: AsyncSession = Depends(get_db)):
    notification_repository = NotificationRepository(session)
    return NotificationService(notification_repository)

def get_subscription_service(session: AsyncSession = Depends(get_db)):
    subscription_repository = SubscriptionRepository(session)
    return SubscriptionService(subscription_repository)

def get_channel_service(session: AsyncSession = Depends(get_db)):
    channel_repository = ChannelRepository(session)
    return ChannelService(channel_repository)

def get_attachment_service(session: AsyncSession = Depends(get_db)):
    attachment_repository = AttachmentRepository(session)
    return AttachmentService(attachment_repository)

def get_schedule_service(session: AsyncSession = Depends(get_db)):
    schedule_repository = ScheduleRepository(session)
    return ScheduleService(schedule_repository)

def get_template_notification_service(session: AsyncSession = Depends(get_db)):
    template_notification_repository = TemplateNotificationRepository(session)
    return TemplateNotificationService(template_notification_repository)

def get_type_notification_service(session: AsyncSession = Depends(get_db)):
    type_notification_repository = TypeNotificationRepository(session)
    return TypeNotificationService(type_notification_repository)