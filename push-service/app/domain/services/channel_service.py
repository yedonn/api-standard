from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import ChannelRepository
from app.schemas.channel import ChannelCreate, ChannelRead, ChannelUpdate


class ChannelService:
    def __init__(self, repository: ChannelRepository):
        self.repository = repository

    # External method: creates a channel, raises HTTPException if necessary
    async def create_channel(self, channel: ChannelCreate) -> ChannelRead:
        db_channel = await self.repository.create(channel)
        return ChannelRead.from_orm(db_channel)

    # External method: raises HTTPException if not found
    async def get_channel_by_id(self, channel_id: int) -> ChannelRead:
        db_channel = await self.repository.get_by_id(channel_id)
        if db_channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return ChannelRead.from_orm(db_channel)

    # Internal method: returns None if not found
    async def get_internal_channel_by_id(self, channel_id: int) -> Optional[ChannelRead]:
        db_channel = await self.repository.get_by_id(channel_id)
        return ChannelRead.from_orm(db_channel) if db_channel else None

    # External method: raises HTTPException if not found
    async def get_channel_by_field(self,  field : str, value: Any) -> ChannelRead:
        db_channel = await self.repository.get_by_field(field, value)
        if db_channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return ChannelRead.from_orm(db_channel)

    # Internal method: returns None if not found
    async def get_internal_channel_by_field(self, field : str, value: Any) -> Optional[ChannelRead]:
        db_channel = await self.repository.get_by_field(field, value)
        return ChannelRead.from_orm(db_channel) if db_channel else None

    # External method: raises HTTPException if no channels found
    async def get_channels(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[ChannelRead]:
        channels = await self.repository.get_all(skip, limit, deleted, order_by)
        if not channels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No channels found")
        return [ChannelRead.from_orm(channel) for channel in channels]

    # Internal method: returns an empty list if no channels found
    async def get_internal_channels(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[ChannelRead]:
        channels = await self.repository.get_all(skip, limit, deleted, order_by)
        return [ChannelRead.from_orm(channel) for channel in channels]

    # External method: raises HTTPException if not found
    async def update_channel(self, channel_id: int, channel_update: ChannelUpdate) -> ChannelRead:
        db_channel = await self.repository.update(channel_id, channel_update)
        if db_channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return ChannelRead.from_orm(db_channel)

    # Internal method: returns None if not found
    async def update_internal_channel(self, channel_id: int, channel_update: ChannelUpdate) -> Optional[ChannelRead]:
        db_channel = await self.repository.update(channel_id, channel_update)
        return ChannelRead.from_orm(db_channel) if db_channel else None

    # External method: raises HTTPException if not found
    async def soft_delete_channel(self, channel_id: int) -> ChannelRead:
        db_channel = await self.repository.update(channel_id, ChannelUpdate(deleted_at=datetime.now()))
        if db_channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return ChannelRead.from_orm(db_channel)

    # Internal method: returns None if not found
    async def soft_delete_internal_channel(self, channel_id: int) -> Optional[ChannelRead]:
        db_channel = await self.repository.update(channel_id, ChannelUpdate(deleted_at=datetime.now()))
        return ChannelRead.from_orm(db_channel) if db_channel else None

    # External method: raises HTTPException if not found
    async def delete_channel(self, channel_id: int) -> ChannelRead:
        db_channel = await self.repository.delete(channel_id)
        if db_channel is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found")
        return ChannelRead.from_orm(db_channel)

    # Internal method: returns None if not found
    async def delete_internal_channel(self, channel_id: int) -> Optional[ChannelRead]:
        db_channel = await self.repository.delete(channel_id)
        return ChannelRead.from_orm(db_channel) if db_channel else None

    # External method: raises HTTPException if no channels found
    async def filter_channels(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[ChannelRead]:
        channels = await self.repository.filter(filters, skip, limit, order_by)
        if not channels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No channels found")
        return [ChannelRead.from_orm(channel) for channel in channels]

    # Internal method: returns empty list if no channels found
    async def filter_internal_channels(self, filters: Dict[str, Any]) -> List[ChannelRead]:
        channels = await self.repository.filter_all(filters)
        return [ChannelRead.from_orm(channel) for channel in channels]

    # New: External method to count channels, raises HTTPException if no channels found
    async def count_channels(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No channels found")
        return count

    # New: Internal method to count channels without raising exceptions
    async def count_internal_channels(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a channel exists, raises HTTPException if not found
    async def exists_channel(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel does not exist")
        return exists

    # New: Internal method to check if a channel exists without raising exceptions
    async def exists_internal_channel(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
