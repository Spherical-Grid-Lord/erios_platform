from pydantic import Field

from core.base import EGPBaseModel
from core.enums import Route
from core.enums import Layer


class RouteItem(EGPBaseModel):

    id: str

    route: Route

    statement: str

    source_layer: Layer

    confidence: float = Field(
        ge=0.0,
        le=1.0
    )

    verified: bool = False


class RouteClassification(EGPBaseModel):

    route_a: list[RouteItem] = []

    route_b: list[RouteItem] = []

    route_c: list[RouteItem] = []
