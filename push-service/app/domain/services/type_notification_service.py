from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import TypeNotificationRepository
from app.schemas.type_notification import TypeNotificationCreate, TypeNotificationRead, TypeNotificationUpdate


class TypeNotificationService:
    def __init__(self, repository: TypeNotificationRepository):
        self.repository = repository

    # External method: creates a type_notification, raises HTTPException if necessary
    async def create_type_notification(self, type_notification: TypeNotificationCreate) -> TypeNotificationRead:
        db_type_notification = await self.repository.create(type_notification)
        return TypeNotificationRead.from_orm(db_type_notification)

    # External method: raises HTTPException if not found
    async def get_type_notification_by_id(self, type_notification_id: int) -> TypeNotificationRead:
        db_type_notification = await self.repository.get_by_id(type_notification_id)
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification not found")
        return TypeNotificationRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def get_internal_type_notification_by_id(self, type_notification_id: int) -> Optional[TypeNotificationRead]:
        db_type_notification = await self.repository.get_by_id(type_notification_id)
        return TypeNotificationRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if not found
    async def get_type_notification_by_field(self,  field : str, value: Any) -> TypeNotificationRead:
        db_type_notification = await self.repository.get_by_field(field, value)
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification not found")
        return TypeNotificationRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def get_internal_type_notification_by_field(self, field : str, value: Any) -> Optional[TypeNotificationRead]:
        db_type_notification = await self.repository.get_by_field(field, value)
        return TypeNotificationRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if no type_notifications found
    async def get_type_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TypeNotificationRead]:
        type_notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        if not type_notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_notifications found")
        return [TypeNotificationRead.from_orm(type_notification) for type_notification in type_notifications]

    # Internal method: returns an empty list if no type_notifications found
    async def get_internal_type_notifications(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[TypeNotificationRead]:
        type_notifications = await self.repository.get_all(skip, limit, deleted, order_by)
        return [TypeNotificationRead.from_orm(type_notification) for type_notification in type_notifications]

    # External method: raises HTTPException if not found
    async def update_type_notification(self, type_notification_id: int, type_notification_update: TypeNotificationUpdate) -> TypeNotificationRead:
        db_type_notification = await self.repository.update(type_notification_id, type_notification_update)
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification not found")
        return TypeNotificationRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def update_internal_type_notification(self, type_notification_id: int, type_notification_update: TypeNotificationUpdate) -> Optional[TypeNotificationRead]:
        db_type_notification = await self.repository.update(type_notification_id, type_notification_update)
        return TypeNotificationRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if not found
    async def soft_delete_type_notification(self, type_notification_id: int) -> TypeNotificationRead:
        db_type_notification = await self.repository.update(type_notification_id, TypeNotificationUpdate(deleted_at=datetime.now()))
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification not found")
        return TypeNotificationRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def soft_delete_internal_type_notification(self, type_notification_id: int) -> Optional[TypeNotificationRead]:
        db_type_notification = await self.repository.update(type_notification_id, TypeNotificationUpdate(deleted_at=datetime.now()))
        return TypeNotificationRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if not found
    async def delete_type_notification(self, type_notification_id: int) -> TypeNotificationRead:
        db_type_notification = await self.repository.delete(type_notification_id)
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification not found")
        return TypeNotificationRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def delete_internal_type_notification(self, type_notification_id: int) -> Optional[TypeNotificationRead]:
        db_type_notification = await self.repository.delete(type_notification_id)
        return TypeNotificationRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if no type_notifications found
    async def filter_type_notifications(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[TypeNotificationRead]:
        type_notifications = await self.repository.filter(filters, skip, limit, order_by)
        if not type_notifications:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_notifications found")
        return [TypeNotificationRead.from_orm(type_notification) for type_notification in type_notifications]

    # Internal method: returns empty list if no type_notifications found
    async def filter_internal_type_notifications(self, filters: Dict[str, Any]) -> List[TypeNotificationRead]:
        type_notifications = await self.repository.filter_all(filters)
        return [TypeNotificationRead.from_orm(type_notification) for type_notification in type_notifications]

    # New: External method to count type_notifications, raises HTTPException if no type_notifications found
    async def count_type_notifications(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No type_notifications found")
        return count

    # New: Internal method to count type_notifications without raising exceptions
    async def count_internal_type_notifications(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a type_notification exists, raises HTTPException if not found
    async def exists_type_notification(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TypeNotification does not exist")
        return exists

    # New: Internal method to check if a type_notification exists without raising exceptions
    async def exists_internal_type_notification(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
