from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_parse_documentation():
    url = "https://petstore.swagger.io/v2/swagger.json"
    response = client.post("/parse", params={"url": url})
    assert response.status_code == 200
    assert "swagger" in response.json()
