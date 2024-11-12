from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import AttachmentRepository
from app.schemas.attachment import AttachmentCreate, AttachmentRead, AttachmentUpdate


class AttachmentService:
    def __init__(self, repository: AttachmentRepository):
        self.repository = repository

    # External method: creates a attachment, raises HTTPException if necessary
    async def create_attachment(self, attachment: AttachmentCreate) -> AttachmentRead:
        db_attachment = await self.repository.create(attachment)
        return AttachmentRead.from_orm(db_attachment)

    # External method: raises HTTPException if not found
    async def get_attachment_by_id(self, attachment_id: int) -> AttachmentRead:
        db_attachment = await self.repository.get_by_id(attachment_id)
        if db_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return AttachmentRead.from_orm(db_attachment)

    # Internal method: returns None if not found
    async def get_internal_attachment_by_id(self, attachment_id: int) -> Optional[AttachmentRead]:
        db_attachment = await self.repository.get_by_id(attachment_id)
        return AttachmentRead.from_orm(db_attachment) if db_attachment else None

    # External method: raises HTTPException if not found
    async def get_attachment_by_field(self,  field : str, value: Any) -> AttachmentRead:
        db_attachment = await self.repository.get_by_field(field, value)
        if db_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return AttachmentRead.from_orm(db_attachment)

    # Internal method: returns None if not found
    async def get_internal_attachment_by_field(self, field : str, value: Any) -> Optional[AttachmentRead]:
        db_attachment = await self.repository.get_by_field(field, value)
        return AttachmentRead.from_orm(db_attachment) if db_attachment else None

    # External method: raises HTTPException if no attachments found
    async def get_attachments(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[AttachmentRead]:
        attachments = await self.repository.get_all(skip, limit, deleted, order_by)
        if not attachments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No attachments found")
        return [AttachmentRead.from_orm(attachment) for attachment in attachments]

    # Internal method: returns an empty list if no attachments found
    async def get_internal_attachments(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[AttachmentRead]:
        attachments = await self.repository.get_all(skip, limit, deleted, order_by)
        return [AttachmentRead.from_orm(attachment) for attachment in attachments]

    # External method: raises HTTPException if not found
    async def update_attachment(self, attachment_id: int, attachment_update: AttachmentUpdate) -> AttachmentRead:
        db_attachment = await self.repository.update(attachment_id, attachment_update)
        if db_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return AttachmentRead.from_orm(db_attachment)

    # Internal method: returns None if not found
    async def update_internal_attachment(self, attachment_id: int, attachment_update: AttachmentUpdate) -> Optional[AttachmentRead]:
        db_attachment = await self.repository.update(attachment_id, attachment_update)
        return AttachmentRead.from_orm(db_attachment) if db_attachment else None

    # External method: raises HTTPException if not found
    async def soft_delete_attachment(self, attachment_id: int) -> AttachmentRead:
        db_attachment = await self.repository.update(attachment_id, AttachmentUpdate(deleted_at=datetime.now()))
        if db_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return AttachmentRead.from_orm(db_attachment)

    # Internal method: returns None if not found
    async def soft_delete_internal_attachment(self, attachment_id: int) -> Optional[AttachmentRead]:
        db_attachment = await self.repository.update(attachment_id, AttachmentUpdate(deleted_at=datetime.now()))
        return AttachmentRead.from_orm(db_attachment) if db_attachment else None

    # External method: raises HTTPException if not found
    async def delete_attachment(self, attachment_id: int) -> AttachmentRead:
        db_attachment = await self.repository.delete(attachment_id)
        if db_attachment is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
        return AttachmentRead.from_orm(db_attachment)

    # Internal method: returns None if not found
    async def delete_internal_attachment(self, attachment_id: int) -> Optional[AttachmentRead]:
        db_attachment = await self.repository.delete(attachment_id)
        return AttachmentRead.from_orm(db_attachment) if db_attachment else None

    # External method: raises HTTPException if no attachments found
    async def filter_attachments(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[AttachmentRead]:
        attachments = await self.repository.filter(filters, skip, limit, order_by)
        if not attachments:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No attachments found")
        return [AttachmentRead.from_orm(attachment) for attachment in attachments]

    # Internal method: returns empty list if no attachments found
    async def filter_internal_attachments(self, filters: Dict[str, Any]) -> List[AttachmentRead]:
        attachments = await self.repository.filter_all(filters)
        return [AttachmentRead.from_orm(attachment) for attachment in attachments]

    # New: External method to count attachments, raises HTTPException if no attachments found
    async def count_attachments(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No attachments found")
        return count

    # New: Internal method to count attachments without raising exceptions
    async def count_internal_attachments(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a attachment exists, raises HTTPException if not found
    async def exists_attachment(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment does not exist")
        return exists

    # New: Internal method to check if a attachment exists without raising exceptions
    async def exists_internal_attachment(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
