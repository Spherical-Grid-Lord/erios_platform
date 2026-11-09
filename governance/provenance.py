from datetime import datetime

from pydantic import Field

from core.base import EGPBaseModel


class Checksum(EGPBaseModel):

    algorithm: str = "sha256"

    value: str


class Provenance(EGPBaseModel):

    source_id: str

    source_type: str

    source_layer: str

    source_uri: str

    checksum: Checksum

    trusted: bool = True

    retrieved_at: datetime = Field(
        default_factory=datetime.utcnow
    )
