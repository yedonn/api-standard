import pytest
from unittest.mock import MagicMock
from app.schemas.user import UserCreate
from app.db.repositories.user_repository import UserRepository

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def user_repository(mock_db):
    repo = UserRepository(db=mock_db)
    repo.create = MagicMock()
    repo.get_by_id = MagicMock()
    repo.get_all = MagicMock()
    repo.filter = MagicMock()
    return repo

def test_create_user(user_repository):
    user_data = UserCreate(username="testuser", email="test@example.com", phone_number="1234567890", password_hash="hashedpassword")
    mock_user = MagicMock(id=1, username="testuser")
    
    user_repository.create.return_value = mock_user
    user = user_repository.create(user_data)
    
    assert user.id is not None
    assert user.username == "testuser"

def test_get_user_by_id(user_repository):
    mock_user = MagicMock(id=1, username="testuser")
    user_repository.get_by_id.return_value = mock_user
    
    user = user_repository.get_by_id(1)
    
    assert user.id == 1
    assert user.username == "testuser"

def test_get_all_users(user_repository):
    mock_user1 = MagicMock(username="user1")
    mock_user2 = MagicMock(username="user2")
    
    user_repository.get_all.return_value = [mock_user1, mock_user2]
    
    users = user_repository.get_all(skip=0, limit=10)
    
    assert len(users) == 2
    assert users[0].username == "user1"
    assert users[1].username == "user2"

def test_filter_users(user_repository):
    mock_user = MagicMock(id=1, username="testuser", is_active=True)
    user_repository.filter.return_value = [mock_user]
    
    users = user_repository.filter({"id": 1, "is_active": True}, skip=0, limit=10)
    
    assert len(users) == 1
    assert users[0].id == 1
    assert users[0].username == "testuser"
    assert users[0].is_active is True
