from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

import pytest
import asyncio
from tests.parallel_tester import run_parallel_tests

def test_parse_documentation():
    url = "https://petstore.swagger.io/v2/swagger.json"
    response = client.post("/parse", params={"url": url})
    assert response.status_code == 200
    assert "swagger" in response.json()

@pytest.mark.anyio
async def test_parallel_endpoint_testing():
    endpoints = ["http://localhost:8000/", "http://localhost:8000/health"]
    results = await run_parallel_tests(endpoints, 10, 1)
    for endpoint, status_code, response_time in results:
        assert status_code == 200
