from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class DeviceModel(Base):
    __tablename__= f"{service}_devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{service}_users.id"), nullable=True)
    device_type = Column(String, nullable=True)
    device_os = Column(String, nullable=True)
    device_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    last_accessed = Column(DateTime, default=func.now())
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)