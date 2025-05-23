from abc import ABC, abstractmethod
from typing import Dict, Any
from app.api.v1.routes.generation.schemas import GenerationRequest, GenerationResponse

class GenerationStrategy(ABC):
    """Base class for all generation strategies."""
    
    @abstractmethod
    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        """Generate content based on the request."""
        pass

    @abstractmethod
    def validate_request(self, request: GenerationRequest) -> None:
        """Validate the request parameters."""
        pass

    @staticmethod
    def get_metadata(request: GenerationRequest) -> Dict[str, Any]:
        """Get metadata for the generation response."""
        return {
            "generation_type": request.generation_type,
            "output_type": request.output_type,
            "search_type": request.search_type
        } 