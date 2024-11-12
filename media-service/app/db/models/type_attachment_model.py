from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class TypeAttachmentModel(Base):
    __tablename__= f"{service}_type_attachments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    table_name = Column(String, unique=True, nullable=True)
    code = Column(String, unique=True, nullable=True)
    name = Column(String, unique=True, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)