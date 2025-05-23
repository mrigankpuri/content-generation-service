import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.routes.generation.schemas import GenerationType, OutputType, SearchType

@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)

@pytest.fixture
def valid_generation_request():
    """Create a valid generation request for testing."""
    return {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content for generation"
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"},
                "metadata": {"type": "object"}
            }
        }
    } 