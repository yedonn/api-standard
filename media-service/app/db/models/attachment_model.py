from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean, Text
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class AttachmentModel(Base):
    __tablename__= f"{service}_Attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type_attachment_id = Column(Integer, ForeignKey(f"{service}_notifications.id"), nullable=True)
    occurence_id = Column(Integer, nullable=True)
    table_name = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    file_url = Column(Text, nullable=True)
    file_type = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)