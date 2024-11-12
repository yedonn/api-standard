from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import ScheduleRepository
from app.schemas.schedule import ScheduleCreate, ScheduleRead, ScheduleUpdate


class ScheduleService:
    def __init__(self, repository: ScheduleRepository):
        self.repository = repository

    # External method: creates a schedule, raises HTTPException if necessary
    async def create_schedule(self, schedule: ScheduleCreate) -> ScheduleRead:
        db_schedule = await self.repository.create(schedule)
        return ScheduleRead.from_orm(db_schedule)

    # External method: raises HTTPException if not found
    async def get_schedule_by_id(self, schedule_id: int) -> ScheduleRead:
        db_schedule = await self.repository.get_by_id(schedule_id)
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return ScheduleRead.from_orm(db_schedule)

    # Internal method: returns None if not found
    async def get_internal_schedule_by_id(self, schedule_id: int) -> Optional[ScheduleRead]:
        db_schedule = await self.repository.get_by_id(schedule_id)
        return ScheduleRead.from_orm(db_schedule) if db_schedule else None

    # External method: raises HTTPException if not found
    async def get_schedule_by_field(self,  field : str, value: Any) -> ScheduleRead:
        db_schedule = await self.repository.get_by_field(field, value)
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return ScheduleRead.from_orm(db_schedule)

    # Internal method: returns None if not found
    async def get_internal_schedule_by_field(self, field : str, value: Any) -> Optional[ScheduleRead]:
        db_schedule = await self.repository.get_by_field(field, value)
        return ScheduleRead.from_orm(db_schedule) if db_schedule else None

    # External method: raises HTTPException if no schedules found
    async def get_schedules(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[ScheduleRead]:
        schedules = await self.repository.get_all(skip, limit, deleted, order_by)
        if not schedules:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No schedules found")
        return [ScheduleRead.from_orm(schedule) for schedule in schedules]

    # Internal method: returns an empty list if no schedules found
    async def get_internal_schedules(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[ScheduleRead]:
        schedules = await self.repository.get_all(skip, limit, deleted, order_by)
        return [ScheduleRead.from_orm(schedule) for schedule in schedules]

    # External method: raises HTTPException if not found
    async def update_schedule(self, schedule_id: int, schedule_update: ScheduleUpdate) -> ScheduleRead:
        db_schedule = await self.repository.update(schedule_id, schedule_update)
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return ScheduleRead.from_orm(db_schedule)

    # Internal method: returns None if not found
    async def update_internal_schedule(self, schedule_id: int, schedule_update: ScheduleUpdate) -> Optional[ScheduleRead]:
        db_schedule = await self.repository.update(schedule_id, schedule_update)
        return ScheduleRead.from_orm(db_schedule) if db_schedule else None

    # External method: raises HTTPException if not found
    async def soft_delete_schedule(self, schedule_id: int) -> ScheduleRead:
        db_schedule = await self.repository.update(schedule_id, ScheduleUpdate(deleted_at=datetime.now()))
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return ScheduleRead.from_orm(db_schedule)

    # Internal method: returns None if not found
    async def soft_delete_internal_schedule(self, schedule_id: int) -> Optional[ScheduleRead]:
        db_schedule = await self.repository.update(schedule_id, ScheduleUpdate(deleted_at=datetime.now()))
        return ScheduleRead.from_orm(db_schedule) if db_schedule else None

    # External method: raises HTTPException if not found
    async def delete_schedule(self, schedule_id: int) -> ScheduleRead:
        db_schedule = await self.repository.delete(schedule_id)
        if db_schedule is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule not found")
        return ScheduleRead.from_orm(db_schedule)

    # Internal method: returns None if not found
    async def delete_internal_schedule(self, schedule_id: int) -> Optional[ScheduleRead]:
        db_schedule = await self.repository.delete(schedule_id)
        return ScheduleRead.from_orm(db_schedule) if db_schedule else None

    # External method: raises HTTPException if no schedules found
    async def filter_schedules(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[ScheduleRead]:
        schedules = await self.repository.filter(filters, skip, limit, order_by)
        if not schedules:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No schedules found")
        return [ScheduleRead.from_orm(schedule) for schedule in schedules]

    # Internal method: returns empty list if no schedules found
    async def filter_internal_schedules(self, filters: Dict[str, Any]) -> List[ScheduleRead]:
        schedules = await self.repository.filter_all(filters)
        return [ScheduleRead.from_orm(schedule) for schedule in schedules]

    # New: External method to count schedules, raises HTTPException if no schedules found
    async def count_schedules(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No schedules found")
        return count

    # New: Internal method to count schedules without raising exceptions
    async def count_internal_schedules(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a schedule exists, raises HTTPException if not found
    async def exists_schedule(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Schedule does not exist")
        return exists

    # New: Internal method to check if a schedule exists without raising exceptions
    async def exists_internal_schedule(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
