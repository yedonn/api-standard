from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import OtpRepository
from app.schemas.otp import OtpCreate, OtpRead, OtpUpdate


class OtpService:
    def __init__(self, repository: OtpRepository):
        self.repository = repository

    # External method: creates a otp, raises HTTPException if necessary
    async def create_otp(self, otp: OtpCreate) -> OtpRead:
        db_otp = await self.repository.create(otp)
        return OtpRead.from_orm(db_otp)

    # External method: raises HTTPException if not found
    async def get_otp_by_id(self, otp_id: int) -> OtpRead:
        db_otp = await self.repository.get_by_id(otp_id)
        if db_otp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otp not found")
        return OtpRead.from_orm(db_otp)

    # Internal method: returns None if not found
    async def get_internal_otp_by_id(self, otp_id: int) -> Optional[OtpRead]:
        db_otp = await self.repository.get_by_id(otp_id)
        return OtpRead.from_orm(db_otp) if db_otp else None

    # External method: raises HTTPException if not found
    async def get_otp_by_field(self,  field : str, value: Any) -> OtpRead:
        db_otp = await self.repository.get_by_field(field, value)
        if db_otp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otp not found")
        return OtpRead.from_orm(db_otp)

    # Internal method: returns None if not found
    async def get_internal_otp_by_field(self, field : str, value: Any) -> Optional[OtpRead]:
        db_otp = await self.repository.get_by_field(field, value)
        return OtpRead.from_orm(db_otp) if db_otp else None

    # External method: raises HTTPException if no otps found
    async def get_otps(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[OtpRead]:
        otps = await self.repository.get_all(skip, limit, deleted, order_by)
        if not otps:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No otps found")
        return [OtpRead.from_orm(otp) for otp in otps]

    # Internal method: returns an empty list if no otps found
    async def get_internal_otps(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[OtpRead]:
        otps = await self.repository.get_all(skip, limit, deleted, order_by)
        return [OtpRead.from_orm(otp) for otp in otps]

    # External method: raises HTTPException if not found
    async def update_otp(self, otp_id: int, otp_update: OtpUpdate) -> OtpRead:
        db_otp = await self.repository.update(otp_id, otp_update)
        if db_otp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otp not found")
        return OtpRead.from_orm(db_otp)

    # Internal method: returns None if not found
    async def update_internal_otp(self, otp_id: int, otp_update: OtpUpdate) -> Optional[OtpRead]:
        db_otp = await self.repository.update(otp_id, otp_update)
        return OtpRead.from_orm(db_otp) if db_otp else None

    # External method: raises HTTPException if not found
    async def delete_otp(self, otp_id: int) -> OtpRead:
        db_otp = await self.repository.delete(otp_id)
        if db_otp is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otp not found")
        return OtpRead.from_orm(db_otp)

    # Internal method: returns None if not found
    async def delete_internal_otp(self, otp_id: int) -> Optional[OtpRead]:
        db_otp = await self.repository.delete(otp_id)
        return OtpRead.from_orm(db_otp) if db_otp else None

    # External method: raises HTTPException if no otps found
    async def filter_otps(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[OtpRead]:
        otps = await self.repository.filter(filters, skip, limit, order_by)
        if not otps:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No otps found")
        return [OtpRead.from_orm(otp) for otp in otps]

    # Internal method: returns empty list if no otps found
    async def filter_internal_otps(self, filters: Dict[str, Any]) -> List[OtpRead]:
        otps = await self.repository.filter_all(filters)
        return [OtpRead.from_orm(otp) for otp in otps]

    # New: External method to count otps, raises HTTPException if no otps found
    async def count_otps(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No otps found")
        return count

    # New: Internal method to count otps without raising exceptions
    async def count_internal_otps(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a otp exists, raises HTTPException if not found
    async def exists_otp(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Otp does not exist")
        return exists

    # New: Internal method to check if a otp exists without raising exceptions
    async def exists_internal_otp(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
