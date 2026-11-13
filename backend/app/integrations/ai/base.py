from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class AIDescriptionProposal(BaseModel):
    text: str = Field(description="Suggested description text")
    model_name: str = Field(description="Name and version of model used")
    tokens_consumed: int = Field(default=0, description="Tokens used for accounting")


class AIProviderAdapter(ABC):
    """Abstract port for multimodal AI models (image + reflection analysis)."""

    @abstractmethod
    async def generate_photo_descriptions(
        self,
        image_bytes: bytes,
        approved_reflection: str | None = None,
        max_alternatives: int = 3,
        max_length: int = 600,
    ) -> list[AIDescriptionProposal]:
        """Analyzes image and reflection to suggest short descriptive alternatives."""
        pass
