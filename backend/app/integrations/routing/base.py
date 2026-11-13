from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class RouteReconstructionResult(BaseModel):
    geometry_geojson: dict[str, Any] = Field(description="LineString GeoJSON")
    estimated_distance_meters: float = Field(description="Estimated path length")
    provider_name: str = Field(description="Underlying routing engine name")


class PedestrianRoutingAdapter(ABC):
    """Abstract port for pedestrian route reconstruction between waypoints."""

    @abstractmethod
    async def calculate_pedestrian_path(
        self, waypoints: list[tuple[float, float]]
    ) -> RouteReconstructionResult:
        """
        Calculates probable pedestrian street route between consecutive GPS points.
        Waypoints are provided as (latitude, longitude) tuples.
        """
        pass
