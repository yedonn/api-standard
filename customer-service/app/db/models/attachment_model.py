from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean, Text
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class AttachmentModel(Base):
    __tablename__= f"{service}_Attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{service}_notifications.id"), nullable=True)
    file_url = Column(Text, nullable=True)
    file_type = Column(String, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())