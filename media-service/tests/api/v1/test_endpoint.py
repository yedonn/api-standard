from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name": "item1", "description": "desc1"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "item1"
    assert data["description"] == "desc1"
