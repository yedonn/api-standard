from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean, Text
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class TemplateNotificationModel(Base):
    __tablename__= f"{service}_template_notifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channel_id = Column(Integer, ForeignKey(f"{service}_channels.id"), nullable=True)
    name = Column(String, nullable=True) # Nom du template (ex : "Bienvenue", "Rappel")
    subject = Column(String, nullable=True) # Sujet pour les emails
    body = Column(Text, nullable=True) # Corps du message (avec potentiels placeholders) {username}, {date}
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)