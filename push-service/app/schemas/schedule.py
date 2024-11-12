from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, time

class ScheduleBase(BaseModel):
    notification_id: int
    frequency: int
    days_of_week: List[int]
    time_of_day: time
    repeat: Optional[bool] = True

class ScheduleCreate(BaseModel):
    notification_id: int
    frequency: int
    days_of_week: List[int]
    time_of_day: time
    repeat: Optional[bool] = None

class ScheduleUpdate(BaseModel):
    notification_id: Optional[int] = None
    frequency: Optional[int] = None
    days_of_week: Optional[List[int]] = None
    time_of_day: Optional[time] = None
    repeat: Optional[bool] = None
    deleted_at: Optional[datetime] = None

class ScheduleRead(ScheduleBase):
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