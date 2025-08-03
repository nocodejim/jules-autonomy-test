from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import fakeredis

from app.cache import get_cache

# Patch get_cache to use fakeredis
fake_redis_client = fakeredis.FakeRedis()
def get_fake_cache():
    return fake_redis_client

app.dependency_overrides[get_cache] = get_fake_cache

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_parse_documentation_caching():
    url = "https://petstore.swagger.io/v2/swagger.json"

    with patch('app.main.parse_openapi') as mock_parse_openapi:
        mock_parse_openapi.return_value = {"swagger": "2.0"}

        # Clear cache before test
        fake_redis_client.flushall()

        # First call
        response1 = client.post("/parse", params={"url": url})
        assert response1.status_code == 200
        assert "swagger" in response1.json()
        mock_parse_openapi.assert_called_once()

        # Second call
        response2 = client.post("/parse", params={"url": url})
        assert response2.status_code == 200
        assert "swagger" in response2.json()
        mock_parse_openapi.assert_called_once() # Should still be called only once

def test_infer_schema_caching():
    api_description = "A simple API with one endpoint that returns a list of users."

    with patch('app.main.infer_schema_from_api') as mock_infer_schema:
        mock_infer_schema.return_value = {"openapi": "3.0.0"}

        # Clear cache before test
        fake_redis_client.flushall()

        # First call
        response1 = client.post("/infer", params={"api_description": api_description})
        assert response1.status_code == 200
        assert "openapi" in response1.json()
        mock_infer_schema.assert_called_once()

        # Second call
        response2 = client.post("/infer", params={"api_description": api_description})
        assert response2.status_code == 200
        assert "openapi" in response2.json()
        mock_infer_schema.assert_called_once() # Should still be called only once
