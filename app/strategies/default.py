from app.api.v1.routes.generation.schemas import GenerationRequest, GenerationType, GenerationResponse, OutputType
from app.core.exceptions import ValidationError
from app.strategies.base import GenerationStrategy


class DefaultStrategy(GenerationStrategy):
    """Default strategy for content generation."""
    
    def validate_request(self, request: GenerationRequest) -> None:
        """Validate default strategy specific parameters."""
        if request.generation_type != GenerationType.DEFAULT:
            raise ValidationError("Invalid generation type for default strategy")
        
        if not request.parameters.get("content"):
            raise ValidationError("Content is required for default generation")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate content using default strategy."""
        self.validate_request(request)
        
        # TODO: Implement actual default generation logic
        return GenerationResponse(
            content="Generated content using default strategy",
            metadata=self.get_metadata(request),
            search_results=[],
            generation_parameters=request.parameters,
            output_schema=request.output_schema if request.output_type == OutputType.JSON else None
        ) 