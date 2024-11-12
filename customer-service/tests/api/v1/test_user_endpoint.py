import pytest
from fastapi import status
from tests.conftest import async_client

@pytest.mark.asyncio
async def test_create_user(async_client):
    print(async_client)
    response = await async_client.post("/api/v1/users/", json={
        "username": "testuser",
        "email": "test@example.com",
        "phone_number": "1234567890",
        "password_hash": "password"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "testuser"

@pytest.mark.asyncio
async def test_get_user(async_client):
    response = await async_client.get("/api/v1/users/1")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_update_user(async_client):
    response = await async_client.put("/api/v1/users/1", json={"username": "updateduser"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "updateduser"

@pytest.mark.asyncio
async def test_delete_user(async_client):
    response = await async_client.delete("/api/v1/users/1")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.asyncio
async def test_get_all_users(async_client):
    response = await async_client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_filter_users(async_client):
    response = await async_client.get("/api/v1/users/search", params={"filters": '{"id":1,"is_active":true}'})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
