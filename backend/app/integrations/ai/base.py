from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class AIDescriptionProposal(BaseModel):
    text: str = Field(description="Suggested description text")
    model_name: str = Field(description="Name and version of model used")
    tokens_consumed: int = Field(default=0, description="Tokens used for accounting")


class AIProviderAdapter(ABC):
    """Backend provider contract for photo descriptions and the trip conclusion."""

    @abstractmethod
    async def generate_photo_descriptions(
        self,
        image_bytes: bytes,
        approved_reflection: str | None = None,
    ) -> list[AIDescriptionProposal]:
        """Suggest descriptions from an authorized EXIF-free derivative."""

    @abstractmethod
    async def draft_trip_conclusion(
        self, approved_reflections: list[str], verified_book_context: str
    ) -> str | None:
        """Draft a synthesis for admin review, or return None for insufficient input."""
