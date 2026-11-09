from pydantic import Field

from core.base import EGPBaseModel
from core.enums import Layer


class LayerObject(EGPBaseModel):

    id: str

    layer: Layer

    source: str

    origin: str | None = None

    content: str = Field(min_length=1)


class LayerClassification(EGPBaseModel):

    layer1_chat: list[LayerObject] = []

    layer2_system: list[LayerObject] = []

    layer3_repository: list[LayerObject] = []

    layer4_internal: list[LayerObject] = []

    layer5_external: list[LayerObject] = []
