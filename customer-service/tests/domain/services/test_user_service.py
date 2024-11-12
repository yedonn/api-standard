import pytest
from unittest.mock import AsyncMock, MagicMock
from app.domain.services.user_service import UserService
from app.schemas.user import UserCreate, UserRead, UserUpdate

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def user_service(mock_db):
    return UserService(db=mock_db)

@pytest.mark.asyncio
async def test_create_user(user_service, user_data, user_read):
    user_service.repository.create = AsyncMock(return_value=user_read)
    result = await user_service.create_user(user_data)
    assert result == user_read

@pytest.mark.asyncio
async def test_get_user_by_id(user_service, user_read):
    user_service.repository.get_by_id = AsyncMock(return_value=user_read)
    result = await user_service.get_user_by_id(1)
    assert result == user_read

@pytest.mark.asyncio
async def test_get_user_all(user_service, user_read):
    user_service.repository.get_all_without_delete = AsyncMock(return_value=[user_read])
    result = await user_service.get_user_all()
    assert result == [user_read]

@pytest.mark.asyncio
async def test_update_user(user_service, user_update, user_read):
    user_service.repository.update = AsyncMock(return_value=user_read)
    result = await user_service.update_user(1, user_update)
    assert result == user_read

@pytest.mark.asyncio
async def test_delete_user(user_service, user_read):
    user_service.repository.delete = AsyncMock(return_value=user_read)
    result = await user_service.delete_user(1)
    assert result == user_read

@pytest.mark.asyncio
async def test_filter_users(user_service, user_read):
    user_service.repository.filter = AsyncMock(return_value=[user_read])
    filters = {"is_active": True}
    result = await user_service.filter_users(filters)
    assert result == [user_read]
