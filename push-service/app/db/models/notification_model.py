from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean, Text
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class NotificationModel(Base):
    __tablename__= f"{service}_notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"customer_users.id"), nullable=True)
    channel_id = Column(Integer, ForeignKey(f"{service}_channels.id"), nullable=True)
    type_notification_id = Column(Integer, ForeignKey(f"{service}_type_notifications.id"), nullable=True)
    title = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    retries = Column(Integer, default=0)
    error_message = Column(Text, nullable=True) # Message d'erreur en cas d'échec d'envoi
    schedule_at = Column(DateTime, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    status = Column(String, default="pending")
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)