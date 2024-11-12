from typing import Optional
from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime

class AttachmentBase(BaseModel):
    table_name: Optional[str] = Field(None, description="Nom de la table liée à l'attachement")
    occurence_id: Optional[int] = Field(None, description="ID de l'occurrence associée")
    type_attachment_id: Optional[int] = Field(None, description="ID du type attachment")
    file_name: Optional[str] = Field(None, description="Nom du fichier attaché")
    file_url: HttpUrl = Field(..., description="URL du fichier attaché")
    file_type: Optional[str] = Field(None, description="Type de fichier (ex: image/png)")
    is_active: Optional[bool] = Field(True, description="Indique si l'attachement est actif")

class AttachmentCreate(AttachmentBase):
    occurence_id: int = Field(..., description="ID d'occurrence requis pour la création")

class AttachmentUpdate(BaseModel):
    table_name: Optional[str] = Field(None, description="Nom de la table liée à l'attachement")
    occurence_id: Optional[int] = Field(None, description="ID de l'occurrence associée")
    file_name: Optional[str] = Field(None, description="Nom du fichier attaché")
    file_url: Optional[HttpUrl] = Field(None, description="URL du fichier attaché")
    file_type: Optional[str] = Field(None, description="Type de fichier (ex: image/png)")
    is_active: Optional[bool] = Field(None, description="Indique si l'attachement est actif")
    deleted_at: Optional[datetime] = Field(None, description="Date de suppression de l'attachement")

class AttachmentRead(AttachmentBase):
    id: int = Field(..., description="ID unique de l'attachement")
    created_at: datetime = Field(..., description="Date de création de l'attachement")
    updated_at: datetime = Field(..., description="Date de la dernière mise à jour de l'attachement")
    deleted_at: Optional[datetime] = Field(None, description="Date de suppression de l'attachement")

    class Config:
        from_attributes = True
        use_enum_values = True
        arbitrary_types_allowed = True
        json_encoders = {
            'sqlalchemy.ext.declarative.api.DeclarativeMeta': lambda obj: BaseModel.from_orm(obj)
        }