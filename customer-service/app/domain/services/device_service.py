from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import DeviceRepository
from app.schemas.device import DeviceCreate, DeviceRead, DeviceUpdate


class DeviceService:
    def __init__(self, repository: DeviceRepository):
        self.repository = repository

    # External method: creates a device, raises HTTPException if necessary
    async def create_device(self, device: DeviceCreate) -> DeviceRead:
        db_device = await self.repository.create(device)
        return DeviceRead.from_orm(db_device)

    # External method: raises HTTPException if not found
    async def get_device_by_id(self, device_id: int) -> DeviceRead:
        db_device = await self.repository.get_by_id(device_id)
        if db_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceRead.from_orm(db_device)

    # Internal method: returns None if not found
    async def get_internal_device_by_id(self, device_id: int) -> Optional[DeviceRead]:
        db_device = await self.repository.get_by_id(device_id)
        return DeviceRead.from_orm(db_device) if db_device else None

    # External method: raises HTTPException if not found
    async def get_device_by_field(self,  field : str, value: Any) -> DeviceRead:
        db_device = await self.repository.get_by_field(field, value)
        if db_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceRead.from_orm(db_device)

    # Internal method: returns None if not found
    async def get_internal_device_by_field(self, field : str, value: Any) -> Optional[DeviceRead]:
        db_device = await self.repository.get_by_field(field, value)
        return DeviceRead.from_orm(db_device) if db_device else None

    # External method: raises HTTPException if no devices found
    async def get_devices(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[DeviceRead]:
        devices = await self.repository.get_all(skip, limit, deleted, order_by)
        if not devices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
        return [DeviceRead.from_orm(device) for device in devices]

    # Internal method: returns an empty list if no devices found
    async def get_internal_devices(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[DeviceRead]:
        devices = await self.repository.get_all(skip, limit, deleted, order_by)
        return [DeviceRead.from_orm(device) for device in devices]

    # External method: raises HTTPException if not found
    async def update_device(self, device_id: int, device_update: DeviceUpdate) -> DeviceRead:
        db_device = await self.repository.update(device_id, device_update)
        if db_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceRead.from_orm(db_device)

    # Internal method: returns None if not found
    async def update_internal_device(self, device_id: int, device_update: DeviceUpdate) -> Optional[DeviceRead]:
        db_device = await self.repository.update(device_id, device_update)
        return DeviceRead.from_orm(db_device) if db_device else None

    # External method: raises HTTPException if not found
    async def delete_device(self, device_id: int) -> DeviceRead:
        db_device = await self.repository.delete(device_id)
        if db_device is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device not found")
        return DeviceRead.from_orm(db_device)

    # Internal method: returns None if not found
    async def delete_internal_device(self, device_id: int) -> Optional[DeviceRead]:
        db_device = await self.repository.delete(device_id)
        return DeviceRead.from_orm(db_device) if db_device else None

    # External method: raises HTTPException if no devices found
    async def filter_devices(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[DeviceRead]:
        devices = await self.repository.filter(filters, skip, limit, order_by)
        if not devices:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
        return [DeviceRead.from_orm(device) for device in devices]

    # Internal method: returns empty list if no devices found
    async def filter_internal_devices(self, filters: Dict[str, Any]) -> List[DeviceRead]:
        devices = await self.repository.filter_all(filters)
        return [DeviceRead.from_orm(device) for device in devices]

    # New: External method to count devices, raises HTTPException if no devices found
    async def count_devices(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No devices found")
        return count

    # New: Internal method to count devices without raising exceptions
    async def count_internal_devices(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a device exists, raises HTTPException if not found
    async def exists_device(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Device does not exist")
        return exists

    # New: Internal method to check if a device exists without raising exceptions
    async def exists_internal_device(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
