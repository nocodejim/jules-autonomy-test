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

def test_infer_schema():
    api_description = "A simple API with one endpoint that returns a list of users."
    response = client.post("/infer", params={"api_description": api_description})
    assert response.status_code == 200
    assert "openapi" in response.json()
