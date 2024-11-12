from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class TypeAttachmentBase(BaseModel):
    table_name: Optional[str] = Field(None, description="Nom de la table liée à ce type d'attachement")
    code: Optional[str] = Field(None, description="Code unique pour le type d'attachement")
    name: Optional[str] = Field(None, description="Nom du type d'attachement")
    description: Optional[str] = Field(None, description="Description du type d'attachement")
    is_active: Optional[bool] = Field(True, description="Indique si le type d'attachement est actif")

class TypeAttachmentCreate(TypeAttachmentBase):
    code: str = Field(..., description="Code unique pour le type d'attachement, requis pour la création")
    name: str = Field(..., description="Nom du type d'attachement, requis pour la création")

class TypeAttachmentUpdate(BaseModel):
    table_name: Optional[str] = Field(None, description="Nom de la table liée à ce type d'attachement")
    code: Optional[str] = Field(None, description="Code unique pour le type d'attachement")
    name: Optional[str] = Field(None, description="Nom du type d'attachement")
    description: Optional[str] = Field(None, description="Description du type d'attachement")
    is_active: Optional[bool] = Field(None, description="Indique si le type d'attachement est actif")
    deleted_at: Optional[datetime] = Field(None, description="Date à laquelle le type d'attachement a été supprimé")

class TypeAttachmentRead(TypeAttachmentBase):
    id: int = Field(..., description="ID unique du type d'attachement")
    created_at: datetime = Field(..., description="Date de création du type d'attachement")
    updated_at: datetime = Field(..., description="Date de la dernière mise à jour du type d'attachement")
    deleted_at: Optional[datetime] = Field(None, description="Date à laquelle le type d'attachement a été supprimé")

    class Config:
        from_attributes = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            'sqlalchemy.ext.declarative.api.DeclarativeMeta': lambda obj: BaseModel.from_orm(obj)
        }
