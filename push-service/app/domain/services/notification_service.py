from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate


class NotificationService:
    def __init__(self, repository: NotificationRepository):
        self.repository = repository

    # External method: creates a notification, raises HTTPException if necessary
    async def create_notification(self, notification: NotificationCreate) -> NotificationRead:
        db_notification = await self.repository.create(notification)
        return NotificationRead.from_orm(db_notification)

    # External method: raises HTTPException if not found
    async def get_notification_by_id(self, notification_id: int) -> NotificationRead:
        db_notification = await self.repository.get_by_id(notification_id)
        if db_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return NotificationRead.from_orm(db_notification)

    # Internal method: returns None if not found
    async def get_internal_notification_by_id(self, notification_id: int) -> Optional[NotificationRead]:
        db_notification = await self.repository.get_by_id(notification_id)
        return NotificationRead.from_orm(db_notification) if db_notification else None

    # External method: raises HTTPException if not found
    async def get_notification_by_field(self,  field : str, value: Any) -> NotificationRead:
        db_notification = await self.repository.get_by_field(field, value)
        if db_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return NotificationRead.from_orm(db_notification)

    # Internal method: returns None if not found
    async def get_internal_notification_by_field(self, field : str, value: Any) -> Optional[NotificationRead]:
        db_notification = await self.repository.get_by_field(field, value)
        return NotificationRead.from_orm(db_notification) if db_notification else None

    # External method: raises HTTPException if no notifications found
    async def get_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[NotificationRead]:
        notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        if not notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
        return [NotificationRead.from_orm(notification) for notification in notifications]

    # Internal method: returns an empty list if no notifications found
    async def get_internal_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[NotificationRead]:
        notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        return [NotificationRead.from_orm(notification) for notification in notifications]

    # External method: raises HTTPException if not found
    async def update_notification(self, notification_id: int, notification_update: NotificationUpdate) -> NotificationRead:
        db_notification = await self.repository.update(notification_id, notification_update)
        if db_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return NotificationRead.from_orm(db_notification)

    # Internal method: returns None if not found
    async def update_internal_notification(self, notification_id: int, notification_update: NotificationUpdate) -> Optional[NotificationRead]:
        db_notification = await self.repository.update(notification_id, notification_update)
        return NotificationRead.from_orm(db_notification) if db_notification else None

    # External method: raises HTTPException if not found
    async def soft_delete_notification(self, notification_id: int) -> NotificationRead:
        db_notification = await self.repository.update(notification_id, NotificationUpdate(deleted_at=datetime.now()))
        if db_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return NotificationRead.from_orm(db_notification)

    # Internal method: returns None if not found
    async def soft_delete_internal_notification(self, notification_id: int) -> Optional[NotificationRead]:
        db_notification = await self.repository.update(notification_id, NotificationUpdate(deleted_at=datetime.now()))
        return NotificationRead.from_orm(db_notification) if db_notification else None

    # External method: raises HTTPException if not found
    async def delete_notification(self, notification_id: int) -> NotificationRead:
        db_notification = await self.repository.delete(notification_id)
        if db_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        return NotificationRead.from_orm(db_notification)

    # Internal method: returns None if not found
    async def delete_internal_notification(self, notification_id: int) -> Optional[NotificationRead]:
        db_notification = await self.repository.delete(notification_id)
        return NotificationRead.from_orm(db_notification) if db_notification else None

    # External method: raises HTTPException if no notifications found
    async def filter_notifications(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[NotificationRead]:
        notifications = await self.repository.filter(filters, skip, limit, order_by)
        if not notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
        return [NotificationRead.from_orm(notification) for notification in notifications]

    # Internal method: returns empty list if no notifications found
    async def filter_internal_notifications(self, filters: Dict[str, Any]) -> List[NotificationRead]:
        notifications = await self.repository.filter_all(filters)
        return [NotificationRead.from_orm(notification) for notification in notifications]

    # New: External method to count notifications, raises HTTPException if no notifications found
    async def count_notifications(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notifications found")
        return count

    # New: Internal method to count notifications without raising exceptions
    async def count_internal_notifications(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a notification exists, raises HTTPException if not found
    async def exists_notification(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification does not exist")
        return exists

    # New: Internal method to check if a notification exists without raising exceptions
    async def exists_internal_notification(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
