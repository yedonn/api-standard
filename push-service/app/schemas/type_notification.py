from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TypeNotificationBase(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

class TypeNotificationCreate(BaseModel):
    code: str = None
    name: str = None
    description: Optional[str] = None
    is_active: Optional[bool] = True

class TypeNotificationUpdate(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    deleted_at: Optional[datetime] = None

class TypeNotificationRead(TypeNotificationBase):
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