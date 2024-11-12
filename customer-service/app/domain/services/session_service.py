from typing import Optional, List, Dict, Any
from fastapi import HTTPException, status
from app.db.repositories.repository import SessionRepository
from app.schemas.session import SessionCreate, SessionRead, SessionUpdate


class SessionService:
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    # External method: creates a session, raises HTTPException if necessary
    async def create_session(self, session: SessionCreate) -> SessionRead:
        db_session = await self.repository.create(session)
        return SessionRead.from_orm(db_session)

    # External method: raises HTTPException if not found
    async def get_session_by_id(self, session_id: int) -> SessionRead:
        db_session = await self.repository.get_by_id(session_id)
        if db_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionRead.from_orm(db_session)

    # Internal method: returns None if not found
    async def get_internal_session_by_id(self, session_id: int) -> Optional[SessionRead]:
        db_session = await self.repository.get_by_id(session_id)
        return SessionRead.from_orm(db_session) if db_session else None

    # External method: raises HTTPException if not found
    async def get_session_by_field(self,  field : str, value: Any) -> SessionRead:
        db_session = await self.repository.get_by_field(field, value)
        if db_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionRead.from_orm(db_session)

    # Internal method: returns None if not found
    async def get_internal_session_by_field(self, field : str, value: Any) -> Optional[SessionRead]:
        db_session = await self.repository.get_by_field(field, value)
        return SessionRead.from_orm(db_session) if db_session else None

    # External method: raises HTTPException if no sessions found
    async def get_sessions(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[SessionRead]:
        sessions = await self.repository.get_all(skip, limit, deleted, order_by)
        if not sessions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found")
        return [SessionRead.from_orm(session) for session in sessions]

    # Internal method: returns an empty list if no sessions found
    async def get_internal_sessions(self, skip: int = 0, limit: int = 10, deleted: bool = False, order_by: str = 'id') -> List[SessionRead]:
        sessions = await self.repository.get_all(skip, limit, deleted, order_by)
        return [SessionRead.from_orm(session) for session in sessions]

    # External method: raises HTTPException if not found
    async def update_session(self, session_id: int, session_update: SessionUpdate) -> SessionRead:
        db_session = await self.repository.update(session_id, session_update)
        if db_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionRead.from_orm(db_session)

    # Internal method: returns None if not found
    async def update_internal_session(self, session_id: int, session_update: SessionUpdate) -> Optional[SessionRead]:
        db_session = await self.repository.update(session_id, session_update)
        return SessionRead.from_orm(db_session) if db_session else None

    # External method: raises HTTPException if not found
    async def delete_session(self, session_id: int) -> SessionRead:
        db_session = await self.repository.delete(session_id)
        if db_session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
        return SessionRead.from_orm(db_session)

    # Internal method: returns None if not found
    async def delete_internal_session(self, session_id: int) -> Optional[SessionRead]:
        db_session = await self.repository.delete(session_id)
        return SessionRead.from_orm(db_session) if db_session else None

    # External method: raises HTTPException if no sessions found
    async def filter_sessions(self, filters: Dict[str, Any], skip: int = 0, limit: int = 10, order_by: str = "id") -> List[SessionRead]:
        sessions = await self.repository.filter(filters, skip, limit, order_by)
        if not sessions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found")
        return [SessionRead.from_orm(session) for session in sessions]

    # Internal method: returns empty list if no sessions found
    async def filter_internal_sessions(self, filters: Dict[str, Any]) -> List[SessionRead]:
        sessions = await self.repository.filter_all(filters)
        return [SessionRead.from_orm(session) for session in sessions]

    # New: External method to count sessions, raises HTTPException if no sessions found
    async def count_sessions(self, filters: Dict[str, Any]) -> int:
        count = await self.repository.count(filters)
        if count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sessions found")
        return count

    # New: Internal method to count sessions without raising exceptions
    async def count_internal_sessions(self, filters: Dict[str, Any]) -> int:
        return await self.repository.count(filters)

    # New: External method to check if a session exists, raises HTTPException if not found
    async def exists_session(self, filters: Dict[str, Any]) -> bool:
        exists = await self.repository.exists(filters)
        if not exists:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session does not exist")
        return exists

    # New: Internal method to check if a session exists without raising exceptions
    async def exists_internal_session(self, filters: Dict[str, Any]) -> bool:
        return await self.repository.exists(filters)
