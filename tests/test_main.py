from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_student():
    response = client.post("/students/", json={
        "name": "Test",
        "age": 20,
        "email": "test@test.com"
    })
    assert response.status_code == 200