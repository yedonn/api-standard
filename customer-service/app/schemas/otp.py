from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class OtpBase(BaseModel):
    user_id: int
    otp_code: str
    verified: Optional[bool] = False

class OtpCreate(BaseModel):
    user_id: int
    otp_code: str
    verified: Optional[bool] = False
    expires_at: datetime

class OtpUpdate(BaseModel):
    verified: Optional[bool] = False

class OtpRead(OtpBase):
    id: int
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            'sqlalchemy.ext.declarative.api.DeclarativeMeta': lambda obj: BaseModel.from_orm(obj)
        }
    # @classmethod
    # def from_orm(cls, obj):
    #     return cls.model_validate(obj)