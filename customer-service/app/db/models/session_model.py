from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class SessionModel(Base):
    __tablename__= f"{service}_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{service}_users.id"), nullable=True)
    device_id = Column(Integer, ForeignKey(f"{service}_devices.id"), nullable=True)
    host = Column(String, nullable=True)
    access_token = Column(String, unique=True, index=True)
    refresh_token = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    
    last_accessed = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)