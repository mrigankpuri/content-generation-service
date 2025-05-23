from typing import Dict, Type

from app.api.v1.routes.generation.schemas import GenerationRequest, GenerationResponse, GenerationType
from app.core.exceptions import ValidationError
from app.strategies.base import GenerationStrategy
from app.strategies.claim_discovery import ClaimDiscoveryStrategy
from app.strategies.default import DefaultStrategy
from app.strategies.evidence_discovery import EvidenceDiscoveryStrategy


class GenerationService:
    """Service for handling content generation requests."""

    def __init__(self):
        self._strategies: Dict[str, Type[GenerationStrategy]] = {GenerationType.CLAIM_DISCOVERY: ClaimDiscoveryStrategy,
                                                                 GenerationType.EVIDENCE_DISCOVERY: EvidenceDiscoveryStrategy,
                                                                 GenerationType.DEFAULT: DefaultStrategy, }

    def get_strategy(self, generation_type: str) -> GenerationStrategy:
        """Get the appropriate generation strategy."""
        strategy_class = self._strategies.get(generation_type)
        if not strategy_class:
            raise ValidationError(f"No strategy found for generation type: {generation_type}")
        return strategy_class()

    async def generate_content(self, request: GenerationRequest) -> GenerationResponse:
        """Generate content using the appropriate strategy."""
        strategy = self.get_strategy(request.generation_type)
        return await strategy.generate(request)
