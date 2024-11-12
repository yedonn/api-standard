from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SubscriptionBase(BaseModel):
    user_id: str
    channel_id: str
    type_notification_id: str
    subscribed: Optional[bool] = True

class SubscriptionCreate(BaseModel):
    user_id: str
    channel_id: str
    type_notification_id: str
    subscribed: Optional[bool] = True

class SubscriptionUpdate(BaseModel):
    user_id: Optional[str] = None
    channel_id: Optional[str] = None
    type_notification_id: Optional[str] = None
    subscribed: Optional[bool] = None
    deleted_at: Optional[datetime] = None

class SubscriptionRead(SubscriptionBase):
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