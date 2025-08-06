from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock
import fakeredis
import pytest

from app.cache import get_cache

# Patch get_cache to use fakeredis
fake_redis_client = fakeredis.FakeRedis()
def get_fake_cache():
    return fake_redis_client

app.dependency_overrides[get_cache] = get_fake_cache

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_cache():
    fake_redis_client.flushall()

def test_discover_endpoint():
    url = "http://example.com"
    with patch('app.main.discover_apis') as mock_discover_apis:
        mock_discover_apis.return_value = ["http://example.com/api/docs"]
        response = client.post("/discover", params={"url": url})
        assert response.status_code == 200
        assert response.json() == {"discovered_urls": ["http://example.com/api/docs"]}
        mock_discover_apis.assert_called_once_with(url)

def test_detect_auth_endpoint():
    schema = {
        "components": {
            "securitySchemes": {
                "apiKey": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-KEY"
                }
            }
        }
    }
    response = client.post("/detect-auth", json=schema)
    assert response.status_code == 200
    assert "detected_schemes" in response.json()
    assert len(response.json()["detected_schemes"]) == 1
    assert response.json()["detected_schemes"][0]["name"] == "apiKey"

@pytest.mark.anyio
async def test_test_endpoints_endpoint():
    schema = {
        "servers": [{"url": "http://testserver"}],
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get users"
                }
            }
        }
    }

    # We need to patch the test_endpoints function in the main module
    with patch('app.main.test_endpoints') as mock_test_endpoints:
        # Since it's an async function, we mock its return value with an awaitable
        mock_test_endpoints.return_value = [
            {
                "method": "GET",
                "url": "http://testserver/users",
                "status_code": 200,
                "reason": "OK"
            }
        ]

        response = client.post("/test-endpoints", json=schema)

        # Check if the mock was called correctly
        mock_test_endpoints.assert_awaited_once_with(schema)

        # Check the response
        assert response.status_code == 200
        assert response.json() == [
            {
                "method": "GET",
                "url": "http://testserver/users",
                "status_code": 200,
                "reason": "OK"
            }
        ]
