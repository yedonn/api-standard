from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel):
    device_type: str
    device_os: str
    device_name: str
    user_id: int 
    is_active: Optional[bool] = True

class DeviceCreate(DeviceBase):
    user_id: Optional[int] = None
    is_active: Optional[bool] = True

class DeviceUpdate(DeviceBase):
    device_type: Optional[str] = None
    device_os: Optional[str] = None
    device_name: Optional[str] = None
    is_active: Optional[bool] = True
    user_id: Optional[int] = None

class DeviceRead(DeviceBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    last_accessed: Optional[datetime] = None

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