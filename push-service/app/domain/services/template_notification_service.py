from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import TemplateNotificationRepository
from app.schemas.template_notification import TemplateNotificationCreate, TemplateNotificationRead, TemplateNotificationUpdate


class TemplateNotificationService:
    def __init__(self, repository: TemplateNotificationRepository):
        self.repository = repository

    # External method: creates a template_notification, raises HTTPException if necessary
    async def create_template_notification(self, template_notification: TemplateNotificationCreate) -> TemplateNotificationRead:
        db_template_notification = await self.repository.create(template_notification)
        return TemplateNotificationRead.from_orm(db_template_notification)

    # External method: raises HTTPException if not found
    async def get_template_notification_by_id(self, template_notification_id: int) -> TemplateNotificationRead:
        db_template_notification = await self.repository.get_by_id(template_notification_id)
        if db_template_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification not found")
        return TemplateNotificationRead.from_orm(db_template_notification)

    # Internal method: returns None if not found
    async def get_internal_template_notification_by_id(self, template_notification_id: int) -> Optional[TemplateNotificationRead]:
        db_template_notification = await self.repository.get_by_id(template_notification_id)
        return TemplateNotificationRead.from_orm(db_template_notification) if db_template_notification else None

    # External method: raises HTTPException if not found
    async def get_template_notification_by_field(self,  field : str, value: Any) -> TemplateNotificationRead:
        db_template_notification = await self.repository.get_by_field(field, value)
        if db_template_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification not found")
        return TemplateNotificationRead.from_orm(db_template_notification)

    # Internal method: returns None if not found
    async def get_internal_template_notification_by_field(self, field : str, value: Any) -> Optional[TemplateNotificationRead]:
        db_template_notification = await self.repository.get_by_field(field, value)
        return TemplateNotificationRead.from_orm(db_template_notification) if db_template_notification else None

    # External method: raises HTTPException if no template_notifications found
    async def get_template_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TemplateNotificationRead]:
        template_notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        if not template_notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No template_notifications found")
        return [TemplateNotificationRead.from_orm(template_notification) for template_notification in template_notifications]

    # Internal method: returns an empty list if no template_notifications found
    async def get_internal_template_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TemplateNotificationRead]:
        template_notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        return [TemplateNotificationRead.from_orm(template_notification) for template_notification in template_notifications]

    # External method: raises HTTPException if not found
    async def update_template_notification(self, template_notification_id: int, template_notification_update: TemplateNotificationUpdate) -> TemplateNotificationRead:
        db_template_notification = await self.repository.update(template_notification_id, template_notification_update)
        if db_template_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification not found")
        return TemplateNotificationRead.from_orm(db_template_notification)

    # Internal method: returns None if not found
    async def update_internal_template_notification(self, template_notification_id: int, template_notification_update: TemplateNotificationUpdate) -> Optional[TemplateNotificationRead]:
        db_template_notification = await self.repository.update(template_notification_id, template_notification_update)
        return TemplateNotificationRead.from_orm(db_template_notification) if db_template_notification else None

    # External method: raises HTTPException if not found
    async def soft_delete_template_notification(self, template_notification_id: int) -> TemplateNotificationRead:
        db_template_notification = await self.repository.update(template_notification_id, TemplateNotificationUpdate(deleted_at=datetime.now()))
        if db_template_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification not found")
        return TemplateNotificationRead.from_orm(db_template_notification)

    # Internal method: returns None if not found
    async def soft_delete_internal_template_notification(self, template_notification_id: int) -> Optional[TemplateNotificationRead]:
        db_template_notification = await self.repository.update(template_notification_id, TemplateNotificationUpdate(deleted_at=datetime.now()))
        return TemplateNotificationRead.from_orm(db_template_notification) if db_template_notification else None

    # External method: raises HTTPException if not found
    async def delete_template_notification(self, template_notification_id: int) -> TemplateNotificationRead:
        db_template_notification = await self.repository.delete(template_notification_id)
        if db_template_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification not found")
        return TemplateNotificationRead.from_orm(db_template_notification)

    # Internal method: returns None if not found
    async def delete_internal_template_notification(self, template_notification_id: int) -> Optional[TemplateNotificationRead]:
        db_template_notification = await self.repository.delete(template_notification_id)
        return TemplateNotificationRead.from_orm(db_template_notification) if db_template_notification else None

    # External method: raises HTTPException if no template_notifications found
    async def filter_template_notifications(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[TemplateNotificationRead]:
        template_notifications = await self.repository.filter(filters, skip, limit, order_by)
        if not template_notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No template_notifications found")
        return [TemplateNotificationRead.from_orm(template_notification) for template_notification in template_notifications]

    # Internal method: returns empty list if no template_notifications found
    async def filter_internal_template_notifications(self, filters: Dict[str, Any]) -> List[TemplateNotificationRead]:
        template_notifications = await self.repository.filter_all(filters)
        return [TemplateNotificationRead.from_orm(template_notification) for template_notification in template_notifications]

    # New: External method to count template_notifications, raises HTTPException if no template_notifications found
    async def count_template_notifications(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No template_notifications found")
        return count

    # New: Internal method to count template_notifications without raising exceptions
    async def count_internal_template_notifications(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a template_notification exists, raises HTTPException if not found
    async def exists_template_notification(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TemplateNotification does not exist")
        return exists

    # New: Internal method to check if a template_notification exists without raising exceptions
    async def exists_internal_template_notification(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
