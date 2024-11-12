from typing import TypeVar, Generic, Optional, Type, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from sqlalchemy import desc, func
from pydantic import BaseModel

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.db = db
        self.model = model

    async def create(self, obj_in: BaseModel) -> T:
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        self.db.add(db_obj)
        try:
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def get_by_id(self, obj_id: int) -> Optional[T]:
        db_obj = await self.db.get(self.model, obj_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
            )
        return db_obj

    async def get_by_field(self, obj_field: str, obj_value: Any) -> Optional[T]:
        query = select(self.model).where(getattr(self.model, obj_field) == obj_value)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def exists(self, obj_field: str, obj_value: Any) -> bool:
        query = select(func.count()).where(getattr(self.model, obj_field) == obj_value)
        result = await self.db.execute(query)
        count = result.scalar()
        return count > 0

    async def count(self, filters: Dict[str, Any] = None) -> int:
        query = select(func.count()).select_from(self.model)
        if filters:
            for field, value in filters.items():
                if hasattr(self.model, field):
                    query = query.where(getattr(self.model, field) == value)
        result = await self.db.execute(query)
        return result.scalar()

    async def get_all(self, skip: int = 0, limit: int = 1000, deleted: bool = False, order_by: str = None) -> List[T]:
        query = select(self.model)

        if deleted:
            query = query.where(self.model.deleted_at != None)
        else:
            query = query.where(self.model.deleted_at == None)

        if order_by:
            direction = desc if order_by.startswith("-") else None
            field_name = order_by.lstrip("-")
            field = getattr(self.model, field_name, None)
            if field:
                query = query.order_by(direction(field)) if direction else query.order_by(field)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update(self, obj_id: int, obj_in: BaseModel) -> Optional[T]:
        db_obj = await self.get_by_id(obj_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
            )
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        try:
            await self.db.commit()
            await self.db.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def delete(self, obj_id: int) -> Optional[T]:
        db_obj = await self.get_by_id(obj_id)
        if not db_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
            )
        try:
            await self.db.delete(db_obj)
            await self.db.commit()
            return db_obj
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    async def filter(self, filters: Dict[str, Any], skip: int = 0, limit: int = 1000, order_by: str = None) -> List[T]:
        query = select(self.model)

        for field, value in filters.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Field '{field}' does not exist in the model")
            if isinstance(value, list):
                query = query.where(getattr(self.model, field).in_(value))
            else:
                query = query.where(getattr(self.model, field) == value)

        if order_by:
            direction = desc if order_by.startswith("-") else None
            field_name = order_by.lstrip("-")
            field = getattr(self.model, field_name, None)
            if field:
                query = query.order_by(direction(field)) if direction else query.order_by(field)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def filter_all(self, filters: Dict[str, Any]) -> List[T]:
        query = select(self.model)

        for field, value in filters.items():
            if not hasattr(self.model, field):
                raise ValueError(f"Field '{field}' does not exist in the model")
            if isinstance(value, list):
                query = query.where(getattr(self.model, field).in_(value))
            else:
                query = query.where(getattr(self.model, field) == value)

        result = await self.db.execute(query)
        return result.scalars().all()
