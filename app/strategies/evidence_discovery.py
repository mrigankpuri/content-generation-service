from app.api.v1.routes.generation.schemas import GenerationRequest, GenerationType, GenerationResponse, OutputType
from app.core.exceptions import ValidationError
from app.strategies.base import GenerationStrategy


class EvidenceDiscoveryStrategy(GenerationStrategy):
    """Strategy for discovering evidence from content."""
    
    def validate_request(self, request: GenerationRequest) -> None:
        """Validate evidence discovery specific parameters."""
        if request.generation_type != GenerationType.EVIDENCE_DISCOVERY:
            raise ValidationError("Invalid generation type for evidence discovery strategy")
        
        if not request.parameters.get("content"):
            raise ValidationError("Content is required for evidence discovery")
        
        if not request.parameters.get("claim"):
            raise ValidationError("Claim is required for evidence discovery")

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate evidence from content."""
        self.validate_request(request)
        
        # TODO: Implement actual evidence discovery logic
        return GenerationResponse(
            content="Discovered evidence from content",
            metadata=self.get_metadata(request),
            search_results=[],
            generation_parameters=request.parameters,
            output_schema=request.output_schema if request.output_type == OutputType.JSON else None
        ) 