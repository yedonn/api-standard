from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class UserInfoModel(Base):
    __tablename__ = f"{service}_user_infos"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{service}_users.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    location = Column(String, nullable=True)
    birthdate = Column(DateTime, nullable=True)
    profile_picture = Column(String, nullable=True)
    country_code = Column(String, nullable=False, default='225')
    phone_number = Column(String, unique=True, index=True, nullable=False)
    whatsapp_country_code = Column(String, nullable=True, default='225')
    whatsapp_phone_number = Column(String, unique=True, index=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    
    # Verification fields
    email_verified = Column(Boolean, default=False)
    phone_number_verified = Column(Boolean, default=False)
    whatsapp_phone_number_verified = Column(Boolean, default=False)
    
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)