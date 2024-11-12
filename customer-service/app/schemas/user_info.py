from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

class UserInfoBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)
    bio: Optional[str] = None
    location: Optional[str] = None
    birthdate: Optional[datetime]
    profile_picture: Optional[str]
    country_code: Optional[str] = "225"
    phone_number: constr(min_length=10, max_length=15)
    whatsapp_country_code: Optional[str] = "225"
    whatsapp_phone_number: Optional[constr(min_length=10, max_length=15)]
    email: EmailStr
    email_verified: Optional[bool] = False
    phone_number_verified: Optional[bool] = False
    whatsapp_phone_number_verified: Optional[bool] = False
    is_active: Optional[bool] = True

class UserInfoCreate(UserInfoBase):
    user_id: int  # Link to the user

class UserInfoUpdate(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)]
    last_name: Optional[constr(min_length=1, max_length=50)]
    bio: Optional[str]
    location: Optional[str]
    birthdate: Optional[datetime]
    profile_picture: Optional[str]
    phone_number: Optional[constr(min_length=10, max_length=15)]
    whatsapp_phone_number: Optional[constr(min_length=10, max_length=15)]
    email: Optional[EmailStr]
    email_verified: Optional[bool]
    phone_number_verified: Optional[bool]
    whatsapp_phone_number_verified: Optional[bool]
    is_active: Optional[bool]

class UserInfoResponse(UserInfoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

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