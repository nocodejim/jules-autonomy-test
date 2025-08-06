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

import logging
import io
import json

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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def test_logging():
    log_stream = io.StringIO()
    logger = logging.getLogger()
    logger.handlers = []
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(logging.Formatter('{"message": "%(message)s"}'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logging.info("test message")

    log_output = log_stream.getvalue()
    log_json = json.loads(log_output)

    assert log_json["message"] == "test message"

def test_create_api():
    response = client.post(
        "/apis/",
        json={"name": "Test API", "description": "A test API", "schema": {"test": "schema"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test API"
    assert data["description"] == "A test API"
    assert data["id"] is not None

def test_read_apis():
    response = client.get("/apis/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

