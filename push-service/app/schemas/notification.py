from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    user_id: int
    channel_id: int
    type_notification_id: int
    title: str
    message: str
    status: str = 'pending'
    retries : Optional[int] = 0
    error_message : Optional[str] = None

class NotificationCreate(NotificationBase):
    schedule_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None

class NotificationUpdate(BaseModel):
    user_id: Optional[int] = None
    channel_id: Optional[int] = None
    type_notification_id: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    retries : Optional[int] = None
    error_message : Optional[str] = None
    schedule_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

class NotificationRead(NotificationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    schedule_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
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