from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TemplateNotificationBase(BaseModel):
    channel_id: Optional[int] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    is_active: Optional[bool] = True

class TemplateNotificationCreate(BaseModel):
    channel_id: int = None
    name: str = None
    subject: Optional[str] = None
    body: Optional[str] = None
    is_active: Optional[bool] = True

class TemplateNotificationUpdate(BaseModel):
    channel_id: Optional[int] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    body: Optional[str] = None
    is_active: Optional[bool] = None
    deleted_at: Optional[datetime] = None

class TemplateNotificationRead(TemplateNotificationBase):
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