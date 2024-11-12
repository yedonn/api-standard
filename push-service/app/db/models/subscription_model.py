from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class SubscriptionModel(Base):
    __tablename__= f"{service}_subscriptions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"customer_users.id"), nullable=True)
    channel_id = Column(Integer, ForeignKey(f"{service}_channels.id"), nullable=True)
    type_notification_id = Column(Integer, ForeignKey(f"{service}_type_notifications.id"), nullable=True)
    subscribed = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)