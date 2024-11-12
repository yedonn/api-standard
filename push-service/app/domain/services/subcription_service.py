from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import SubscriptionRepository
from app.schemas.subscription import SubscriptionCreate, SubscriptionRead, SubscriptionUpdate


class SubscriptionService:
    def __init__(self, repository: SubscriptionRepository):
        self.repository = repository

    # External method: creates a subscription, raises HTTPException if necessary
    async def create_subscription(self, subscription: SubscriptionCreate) -> SubscriptionRead:
        db_subscription = await self.repository.create(subscription)
        return SubscriptionRead.from_orm(db_subscription)

    # External method: raises HTTPException if not found
    async def get_subscription_by_id(self, subscription_id: int) -> SubscriptionRead:
        db_subscription = await self.repository.get_by_id(subscription_id)
        if db_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return SubscriptionRead.from_orm(db_subscription)

    # Internal method: returns None if not found
    async def get_internal_subscription_by_id(self, subscription_id: int) -> Optional[SubscriptionRead]:
        db_subscription = await self.repository.get_by_id(subscription_id)
        return SubscriptionRead.from_orm(db_subscription) if db_subscription else None

    # External method: raises HTTPException if not found
    async def get_subscription_by_field(self,  field : str, value: Any) -> SubscriptionRead:
        db_subscription = await self.repository.get_by_field(field, value)
        if db_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return SubscriptionRead.from_orm(db_subscription)

    # Internal method: returns None if not found
    async def get_internal_subscription_by_field(self, field : str, value: Any) -> Optional[SubscriptionRead]:
        db_subscription = await self.repository.get_by_field(field, value)
        return SubscriptionRead.from_orm(db_subscription) if db_subscription else None

    # External method: raises HTTPException if no subscriptions found
    async def get_subscriptions(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[SubscriptionRead]:
        subscriptions = await self.repository.get_all(skip, limit, deleted, order_by)
        if not subscriptions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscriptions found")
        return [SubscriptionRead.from_orm(subscription) for subscription in subscriptions]

    # Internal method: returns an empty list if no subscriptions found
    async def get_internal_subscriptions(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[SubscriptionRead]:
        subscriptions = await self.repository.get_all(skip, limit, deleted, order_by)
        return [SubscriptionRead.from_orm(subscription) for subscription in subscriptions]

    # External method: raises HTTPException if not found
    async def update_subscription(self, subscription_id: int, subscription_update: SubscriptionUpdate) -> SubscriptionRead:
        db_subscription = await self.repository.update(subscription_id, subscription_update)
        if db_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return SubscriptionRead.from_orm(db_subscription)

    # Internal method: returns None if not found
    async def update_internal_subscription(self, subscription_id: int, subscription_update: SubscriptionUpdate) -> Optional[SubscriptionRead]:
        db_subscription = await self.repository.update(subscription_id, subscription_update)
        return SubscriptionRead.from_orm(db_subscription) if db_subscription else None

    # External method: raises HTTPException if not found
    async def soft_delete_subscription(self, type_notification_id: int) -> SubscriptionRead:
        db_type_notification = await self.repository.update(type_notification_id, SubscriptionUpdate(deleted_at=datetime.now()))
        if db_type_notification is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return SubscriptionRead.from_orm(db_type_notification)

    # Internal method: returns None if not found
    async def soft_delete_internal_type_notification(self, type_notification_id: int) -> Optional[SubscriptionRead]:
        db_type_notification = await self.repository.update(type_notification_id, SubscriptionUpdate(deleted_at=datetime.now()))
        return SubscriptionRead.from_orm(db_type_notification) if db_type_notification else None

    # External method: raises HTTPException if not found
    async def delete_subscription(self, subscription_id: int) -> SubscriptionRead:
        db_subscription = await self.repository.delete(subscription_id)
        if db_subscription is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
        return SubscriptionRead.from_orm(db_subscription)

    # Internal method: returns None if not found
    async def delete_internal_subscription(self, subscription_id: int) -> Optional[SubscriptionRead]:
        db_subscription = await self.repository.delete(subscription_id)
        return SubscriptionRead.from_orm(db_subscription) if db_subscription else None

    # External method: raises HTTPException if no subscriptions found
    async def filter_subscriptions(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[SubscriptionRead]:
        subscriptions = await self.repository.filter(filters, skip, limit, order_by)
        if not subscriptions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscriptions found")
        return [SubscriptionRead.from_orm(subscription) for subscription in subscriptions]

    # Internal method: returns empty list if no subscriptions found
    async def filter_internal_subscriptions(self, filters: Dict[str, Any]) -> List[SubscriptionRead]:
        subscriptions = await self.repository.filter_all(filters)
        return [SubscriptionRead.from_orm(subscription) for subscription in subscriptions]

    # New: External method to count subscriptions, raises HTTPException if no subscriptions found
    async def count_subscriptions(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No subscriptions found")
        return count

    # New: Internal method to count subscriptions without raising exceptions
    async def count_internal_subscriptions(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a subscription exists, raises HTTPException if not found
    async def exists_subscription(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription does not exist")
        return exists

    # New: Internal method to check if a subscription exists without raising exceptions
    async def exists_internal_subscription(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
