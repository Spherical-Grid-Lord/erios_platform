from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class EGPBaseModel(BaseModel):

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
        use_enum_values=True
    )


class AuditMixin(EGPBaseModel):

    id: UUID = Field(default_factory=uuid4)

    created_at: datetime = Field(
        default_factory=datetime.utcnow
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow
    )
