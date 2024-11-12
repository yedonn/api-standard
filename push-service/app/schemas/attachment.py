from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class AttachmentBase(BaseModel):
    notification_id: Optional[int] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    is_active: Optional[bool] = True

class AttachmentCreate(BaseModel):
    notification_id: int = None
    file_url: str = None
    file_type: Optional[str] = None
    is_active: Optional[bool] = True

class AttachmentUpdate(BaseModel):
    notification_id: Optional[int] = None
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    is_active: Optional[bool] = None
    deleted_at: Optional[datetime] = None

class AttachmentRead(AttachmentBase):
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