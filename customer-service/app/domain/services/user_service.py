from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # External method: creates a user, raises HTTPException if necessary
    async def create_user(self, user: UserCreate) -> UserRead:
        db_user = await self.repository.create(user)
        return UserRead.from_orm(db_user)

    # External method: raises HTTPException if not found
    async def get_user_by_id(self, user_id: int) -> UserRead:
        db_user = await self.repository.get_by_id(user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.from_orm(db_user)

    # Internal method: returns None if not found
    async def get_internal_user_by_id(self, user_id: int) -> Optional[UserRead]:
        db_user = await self.repository.get_by_id(user_id)
        return UserRead.from_orm(db_user) if db_user else None

    # External method: raises HTTPException if not found
    async def get_user_by_field(self,  field : str, value: Any) -> UserRead:
        db_user = await self.repository.get_by_field(field, value)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.from_orm(db_user)

    # Internal method: returns None if not found
    async def get_internal_user_by_field(self, field : str, value: Any) -> Optional[UserRead]:
        db_user = await self.repository.get_by_field(field, value)
        return UserRead.from_orm(db_user) if db_user else None

    # External method: raises HTTPException if no users found
    async def get_users(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[UserRead]:
        users = await self.repository.get_all(skip, limit, deleted, order_by)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return [UserRead.from_orm(user) for user in users]

    # Internal method: returns an empty list if no users found
    async def get_internal_users(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[UserRead]:
        users = await self.repository.get_all(skip, limit, deleted, order_by)
        return [UserRead.from_orm(user) for user in users]

    # External method: raises HTTPException if not found
    async def update_user(self, user_id: int, user_update: UserUpdate) -> UserRead:
        db_user = await self.repository.update(user_id, user_update)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.from_orm(db_user)

    # Internal method: returns None if not found
    async def update_internal_user(self, user_id: int, user_update: UserUpdate) -> Optional[UserRead]:
        db_user = await self.repository.update(user_id, user_update)
        return UserRead.from_orm(db_user) if db_user else None

    # External method: raises HTTPException if not found
    async def soft_delete_user(self, user_id: int) -> UserRead:
        db_user = await self.repository.update(user_id, UserUpdate(deleted_at=datetime.now()))
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.from_orm(db_user)

    # Internal method: returns None if not found
    async def soft_delete_internal_user(self, user_id: int) -> Optional[UserRead]:
        db_user = await self.repository.update(user_id, UserUpdate(deleted_at=datetime.now()))
        return UserRead.from_orm(db_user) if db_user else None

    # External method: raises HTTPException if not found
    async def delete_user(self, user_id: int) -> UserRead:
        db_user = await self.repository.delete(user_id)
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return UserRead.from_orm(db_user)

    # Internal method: returns None if not found
    async def delete_internal_user(self, user_id: int) -> Optional[UserRead]:
        db_user = await self.repository.delete(user_id)
        return UserRead.from_orm(db_user) if db_user else None

    # External method: raises HTTPException if no users found
    async def filter_users(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[UserRead]:
        users = await self.repository.filter(filters, skip, limit, order_by)
        if not users:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return [UserRead.from_orm(user) for user in users]

    # Internal method: returns empty list if no users found
    async def filter_internal_users(self, filters: Dict[str, Any]) -> List[UserRead]:
        users = await self.repository.filter_all(filters)
        return [UserRead.from_orm(user) for user in users]

    # New: External method to count users, raises HTTPException if no users found
    async def count_users(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
        return count

    # New: Internal method to count users without raising exceptions
    async def count_internal_users(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a user exists, raises HTTPException if not found
    async def exists_user(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")
        return exists

    # New: Internal method to check if a user exists without raising exceptions
    async def exists_internal_user(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
