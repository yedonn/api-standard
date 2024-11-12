from app.db.database import Base
from sqlalchemy.orm import relationship

from app.db.models.subscription_model import SubscriptionModel
from app.db.models.schedule_model import ScheduleModel
from app.db.models.notification_model import NotificationModel
from app.db.models.type_notification_model import TypeNotificationModel
from app.db.models.template_notification_model import TemplateNotificationModel
from app.db.models.attachment_model import AttachmentModel
from app.db.models.channel_model import ChannelModel


SubscriptionModel.user = relationship('UserModel')
SubscriptionModel.channel = relationship('ChannelModel')

ScheduleModel.notification = relationship('NotificationModel')

NotificationModel.user = relationship('UserModel')
NotificationModel.channel = relationship('ChannelModel')
NotificationModel.type_notification = relationship('TypeNotificationModel')

AttachmentModel.notification = relationship('NotificationModel')