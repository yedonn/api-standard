from sqlalchemy import Column, Integer, String, ForeignKey, DateTime ,Boolean
from app.db.database import Base
from sqlalchemy.sql import func
from app.core.config import settings

service=settings.SERVICE_NAME.split(" ")[0].lower()
class OtpModel(Base):
    __tablename__= f"{service}_otps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(f"{service}_users.id"), nullable=True)
    otp_code = Column(String, unique=True, index=True)
    retries = Column(Integer, default=0)
    verified = Column(Boolean, default=False)
    
    
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime)