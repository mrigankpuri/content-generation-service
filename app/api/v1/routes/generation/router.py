from fastapi import APIRouter, Depends, HTTPException
from app.api.v1.routes.generation.schemas import GenerationRequest, GenerationResponse
from app.services.generation import GenerationService
from app.core.exceptions import GenerationError, ValidationError
from app.api.v1.routes.generation.dependencies import get_generation_service

router = APIRouter()

def validate_output_schema(request: GenerationRequest) -> None:
    if request.output_type == "json":
        if not request.output_schema or not isinstance(request.output_schema, dict):
            raise HTTPException(status_code=422, detail="output_schema must be a non-empty dictionary when output_type is JSON")
    elif request.output_schema is not None:
        raise HTTPException(status_code=422, detail="output_schema should not be provided when output_type is not JSON")

@router.post("/generate", response_model=GenerationResponse)
async def generate_content(
    request: GenerationRequest,
    generation_service: GenerationService = Depends(get_generation_service)
) -> GenerationResponse:
    """Generate content based on the request."""
    validate_output_schema(request)
    try:
        return await generation_service.generate_content(request)
    except ValidationError as e:
        raise e
    except Exception as e:
        raise GenerationError(f"Failed to generate content: {str(e)}") 