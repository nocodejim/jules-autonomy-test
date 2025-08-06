from fastapi.testclient import TestClient
from app.main import app
import pytest

client = TestClient(app)

@pytest.fixture
def sample_openapi_schema():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Simple API",
            "version": "1.0.0"
        },
        "paths": {
            "/users": {
                "get": {
                    "summary": "Get a list of users",
                    "operationId": "get_users",
                    "responses": {
                        "200": {
                            "description": "A list of users",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/User"
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "User": {
                    "type": "object",
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        }
                    },
                    "required": ["id", "name"]
                }
            }
        }
    }

def test_generate_python_sdk(sample_openapi_schema):
    response = client.post("/generate-sdk/python", json=sample_openapi_schema)
    assert response.status_code == 200
    sdk_code = response.json().get("sdk")
    assert sdk_code is not None
    assert "class MyApiClient" in sdk_code
    assert "def get_users(self)" in sdk_code
    assert "class User(BaseModel):" in sdk_code
    assert "id: int" in sdk_code
    assert "name: str" in sdk_code

    # Check if the generated code is valid Python
    try:
        compile(sdk_code, "<string>", "exec")
    except SyntaxError as e:
        pytest.fail(f"Generated SDK has a syntax error: {e}\n--- CODE ---\n{sdk_code}")
