from typing import Optional
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr
    phone_number: constr(min_length=10, max_length=15)
    country_code: Optional[str] = "225"
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: constr(min_length=6)

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)]
    email: Optional[EmailStr]
    phone_number: Optional[constr(min_length=10, max_length=15)]
    country_code: Optional[str]
    is_active: Optional[bool]

class UserRead(UserBase):
    id: int
    password: Optional[str] = None
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