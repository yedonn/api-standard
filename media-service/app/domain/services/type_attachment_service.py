from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import TypeAttachmentRepository
from app.schemas.type_attachment import TypeAttachmentCreate, TypeAttachmentRead, TypeAttachmentUpdate


class TypeAttachmentService:
    def __init__(self, repository: TypeAttachmentRepository):
        self.repository = repository

    # External method: creates a type_attachment, raises HTTPException if necessary
    async def create_type_attachment(self, type_attachment: TypeAttachmentCreate) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.create(type_attachment)
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # External method: raises HTTPException if not found
    async def get_type_attachment_by_id(self, type_attachment_id: int) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.get_by_id(type_attachment_id)
        if db_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # Internal method: returns None if not found
    async def get_internal_type_attachment_by_id(self, type_attachment_id: int) -> Optional[TypeAttachmentRead]:
        db_type_attachment = await self.repository.get_by_id(type_attachment_id)
        return TypeAttachmentRead.from_orm(db_type_attachment) if db_type_attachment else None

    # External method: raises HTTPException if not found
    async def get_type_attachment_by_field(self,  field : str, value: Any) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.get_by_field(field, value)
        if db_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # Internal method: returns None if not found
    async def get_internal_type_attachment_by_field(self, field : str, value: Any) -> Optional[TypeAttachmentRead]:
        db_type_attachment = await self.repository.get_by_field(field, value)
        return TypeAttachmentRead.from_orm(db_type_attachment) if db_type_attachment else None

    # External method: raises HTTPException if no type_attachments found
    async def get_type_attachments(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TypeAttachmentRead]:
        type_attachments = await self.repository.get_all(skip, limit, deleted, order_by)
        if not type_attachments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_attachments found")
        return [TypeAttachmentRead.from_orm(type_attachment) for type_attachment in type_attachments]

    # Internal method: returns an empty list if no type_attachments found
    async def get_internal_type_attachments(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TypeAttachmentRead]:
        type_attachments = await self.repository.get_all(skip, limit, deleted, order_by)
        return [TypeAttachmentRead.from_orm(type_attachment) for type_attachment in type_attachments]

    # External method: raises HTTPException if not found
    async def update_type_attachment(self, type_attachment_id: int, type_attachment_update: TypeAttachmentUpdate) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.update(type_attachment_id, type_attachment_update)
        if db_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # Internal method: returns None if not found
    async def update_internal_type_attachment(self, type_attachment_id: int, type_attachment_update: TypeAttachmentUpdate) -> Optional[TypeAttachmentRead]:
        db_type_attachment = await self.repository.update(type_attachment_id, type_attachment_update)
        return TypeAttachmentRead.from_orm(db_type_attachment) if db_type_attachment else None

    # External method: raises HTTPException if not found
    async def soft_delete_type_attachment(self, type_attachment_id: int) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.update(type_attachment_id, TypeAttachmentUpdate(deleted_at=datetime.now()))
        if db_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # Internal method: returns None if not found
    async def soft_delete_internal_type_attachment(self, type_attachment_id: int) -> Optional[TypeAttachmentRead]:
        db_type_attachment = await self.repository.update(type_attachment_id, TypeAttachmentUpdate(deleted_at=datetime.now()))
        return TypeAttachmentRead.from_orm(db_type_attachment) if db_type_attachment else None

    # External method: raises HTTPException if not found
    async def delete_type_attachment(self, type_attachment_id: int) -> TypeAttachmentRead:
        db_type_attachment = await self.repository.delete(type_attachment_id)
        if db_type_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment not found")
        return TypeAttachmentRead.from_orm(db_type_attachment)

    # Internal method: returns None if not found
    async def delete_internal_type_attachment(self, type_attachment_id: int) -> Optional[TypeAttachmentRead]:
        db_type_attachment = await self.repository.delete(type_attachment_id)
        return TypeAttachmentRead.from_orm(db_type_attachment) if db_type_attachment else None

    # External method: raises HTTPException if no type_attachments found
    async def filter_type_attachments(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[TypeAttachmentRead]:
        type_attachments = await self.repository.filter(filters, skip, limit, order_by)
        if not type_attachments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_attachments found")
        return [TypeAttachmentRead.from_orm(type_attachment) for type_attachment in type_attachments]

    # Internal method: returns empty list if no type_attachments found
    async def filter_internal_type_attachments(self, filters: Dict[str, Any]) -> List[TypeAttachmentRead]:
        type_attachments = await self.repository.filter_all(filters)
        return [TypeAttachmentRead.from_orm(type_attachment) for type_attachment in type_attachments]

    # New: External method to count type_attachments, raises HTTPException if no type_attachments found
    async def count_type_attachments(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_attachments found")
        return count

    # New: Internal method to count type_attachments without raising exceptions
    async def count_internal_type_attachments(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a type_attachment exists, raises HTTPException if not found
    async def exists_type_attachment(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeAttachment does not exist")
        return exists

    # New: Internal method to check if a type_attachment exists without raising exceptions
    async def exists_internal_type_attachment(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
