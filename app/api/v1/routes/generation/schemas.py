from enum import Enum
from typing import Dict, Any, List, Optional

from pydantic import BaseModel, Field, model_validator, field_validator


class GenerationType(str, Enum):
    """Types of content generation."""
    CLAIM_DISCOVERY = "claim_discovery"
    EVIDENCE_DISCOVERY = "evidence_discovery"
    DEFAULT = "default"


class OutputType(str, Enum):
    """Types of output formats."""
    JSON = "json"
    TEXT = "text"


class SearchType(str, Enum):
    """Types of search operations."""
    SELECTED_FILES = "selected_files"
    GLOBAL = "global"


class BaseResponseModel(BaseModel):
    """Base model for all responses that require output schema validation."""
    output_schema: Optional[Dict[str, Any]] = Field(
        None, description="Schema defining the expected structure of the response"
    )

    @field_validator("output_schema")
    def validate_output_schema(cls, v):
        if v is not None and not isinstance(v, dict):
            raise ValueError("output_schema must be a dictionary when provided")
        return v


class GenerationRequest(BaseModel):
    """Request model for content generation."""
    generation_type: GenerationType = Field(
        ..., description="Type of content to generate"
    )
    output_type: OutputType = Field(
        default=OutputType.JSON, description="Desired output format"
    )
    search_type: SearchType = Field(
        default=SearchType.GLOBAL, description="Type of search to perform"
    )
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Generation parameters"
    )
    output_schema: Optional[Dict[str, Any]] = Field(
        None,
        description="Schema defining the expected structure of the response (required for JSON output)",
    )

    @model_validator(mode="after")
    def check_output_schema_required_for_json(self):
        if self.output_type == OutputType.JSON:
            if not self.output_schema or not isinstance(self.output_schema, dict):
                raise ValueError(
                    "output_schema must be a non-empty dictionary when output_type is JSON"
                )
        elif self.output_schema is not None:
            raise ValueError(
                "output_schema should not be provided when output_type is not JSON"
            )
        return self


class GenerationResponse(BaseResponseModel):
    """Response model for content generation."""
    content: str = Field(..., description="Generated content")
    metadata: Dict[str, Any] = Field(..., description="Generation metadata")
    search_results: List[Dict[str, Any]] = Field(
        default_factory=list, description="Search results used"
    )
    generation_parameters: Dict[str, Any] = Field(
        ..., description="Parameters used for generation"
    )
