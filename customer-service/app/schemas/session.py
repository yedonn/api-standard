from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class SessionBase(BaseModel):
    user_id: int
    device_id: int
    access_token: str
    refresh_token: str
    host: str
    expires_at: datetime
    is_active: Optional[bool]= True

class SessionCreate(SessionBase):
    pass

class SessionUpdate(BaseModel):
    user_id: Optional[int] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    host: Optional[str] = None
    device: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class SessionRead(SessionBase):
    id: int
    created_at: datetime
    last_accessed: Optional[datetime] = None
    
    class Config:
        from_attributes = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            'sqlalchemy.ext.declarative.api.DeclarativeMeta': lambda obj: BaseModel.from_orm(obj)
        }