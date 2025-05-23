from fastapi.testclient import TestClient

from app.api.v1.routes.generation.schemas import GenerationType, OutputType, SearchType
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_content_default():
    """Test the default content generation flow."""
    request_data = {
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
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "content" in result
    assert "metadata" in result
    assert "search_results" in result
    assert "generation_parameters" in result
    assert "output_schema" in result
    
    # Validate metadata
    metadata = result["metadata"]
    assert metadata["generation_type"] == GenerationType.DEFAULT
    assert metadata["output_type"] == OutputType.JSON
    assert metadata["search_type"] == SearchType.GLOBAL

def test_generate_content_text_output():
    """Test content generation with text output type."""
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.TEXT,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content for generation"
        }
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "content" in result
    assert "metadata" in result
    assert "search_results" in result
    assert "generation_parameters" in result
    assert result.get("output_schema") is None

def test_generate_content_validation():
    """Test validation of the generation request."""
    # Test missing required content parameter
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {},  # Missing content
        "output_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"}
            }
        }
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 400
    assert "Content is required" in response.json()["detail"]

def test_generate_content_invalid_type():
    """Test invalid generation type handling."""
    request_data = {
        "generation_type": "invalid_type",  # Invalid type
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content"
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"}
            }
        }
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 422  # Validation error

def test_generate_content_missing_schema_for_json():
    """Test validation when output schema is missing for JSON output type."""
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content"
        }
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 422
    assert "Value error, output_schema must be a non-empty dictionary when output_type is JSON" in response.json()["detail"][0]["msg"]

def test_generate_content_schema_for_text():
    """Test validation when output schema is provided for TEXT output type."""
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.TEXT,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content"
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "content": {"type": "string"}
            }
        }
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 422
    assert "Value error, output_schema should not be provided when output_type is not JSON" in response.json()["detail"][0]["msg"]

def test_generate_content_empty_schema():
    """Test validation with empty output schema."""
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content"
        },
        "output_schema": {}  # Empty schema
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 422
    assert "Value error, output_schema must be a non-empty dictionary when output_type is JSON" in response.json()["detail"][0]["msg"]

def test_generate_content_default_strategy():
    """Test the default strategy implementation."""
    from app.strategies.default import DefaultStrategy
    from app.api.v1.routes.generation.schemas import GenerationRequest
    
    strategy = DefaultStrategy()
    request = GenerationRequest(
        generation_type=GenerationType.DEFAULT,
        output_type=OutputType.JSON,
        search_type=SearchType.GLOBAL,
        parameters={"content": "Test content"},
        output_schema={
            "type": "object",
            "properties": {
                "content": {"type": "string"}
            }
        }
    )
    
    # Test validation
    strategy.validate_request(request)
    
    # Test generation
    import asyncio
    response = asyncio.run(strategy.generate(request))
    assert isinstance(response.content, str)
    assert isinstance(response.metadata, dict)
    assert isinstance(response.search_results, list)
    assert isinstance(response.generation_parameters, dict)
    assert isinstance(response.output_schema, dict)

def test_generate_content_claim_discovery():
    """Test the claim discovery strategy implementation."""
    from app.strategies.claim_discovery import ClaimDiscoveryStrategy
    from app.api.v1.routes.generation.schemas import GenerationRequest
    
    strategy = ClaimDiscoveryStrategy()
    request = GenerationRequest(
        generation_type=GenerationType.CLAIM_DISCOVERY,
        output_type=OutputType.JSON,
        search_type=SearchType.GLOBAL,
        parameters={"content": "Test content"},
        output_schema={
            "type": "object",
            "properties": {
                "claims": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    )
    
    # Test validation
    strategy.validate_request(request)
    
    # Test generation
    import asyncio
    response = asyncio.run(strategy.generate(request))
    assert isinstance(response.content, str)
    assert isinstance(response.metadata, dict)
    assert isinstance(response.search_results, list)
    assert isinstance(response.generation_parameters, dict)
    assert isinstance(response.output_schema, dict)
    assert response.metadata["generation_type"] == GenerationType.CLAIM_DISCOVERY

def test_generate_content_evidence_discovery():
    """Test the evidence discovery strategy implementation."""
    from app.strategies.evidence_discovery import EvidenceDiscoveryStrategy
    from app.api.v1.routes.generation.schemas import GenerationRequest
    
    strategy = EvidenceDiscoveryStrategy()
    request = GenerationRequest(
        generation_type=GenerationType.EVIDENCE_DISCOVERY,
        output_type=OutputType.JSON,
        search_type=SearchType.GLOBAL,
        parameters={
            "content": "Test content",
            "claim": "Test claim"
        },
        output_schema={
            "type": "object",
            "properties": {
                "evidence": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    )
    
    # Test validation
    strategy.validate_request(request)
    
    # Test generation
    import asyncio
    response = asyncio.run(strategy.generate(request))
    assert isinstance(response.content, str)
    assert isinstance(response.metadata, dict)
    assert isinstance(response.search_results, list)
    assert isinstance(response.generation_parameters, dict)
    assert isinstance(response.output_schema, dict)
    assert response.metadata["generation_type"] == GenerationType.EVIDENCE_DISCOVERY

def test_generate_content_invalid_schema():
    """Test validation with invalid output schema format."""
    request_data = {
        "generation_type": GenerationType.DEFAULT,
        "output_type": OutputType.JSON,
        "search_type": SearchType.GLOBAL,
        "parameters": {
            "content": "Test content"
        },
        "output_schema": "invalid_schema"  # Should be a dictionary
    }
    
    response = client.post("/api/v1/generation/generate", json=request_data)
    assert response.status_code == 422
    assert "output_schema" in response.json()["detail"][0]["loc"]
    assert "Input should be a valid dictionary" in response.json()["detail"][0]["msg"] 