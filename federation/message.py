from typing import Any

from core.base import EGPBaseModel


class MCPEnvelope(EGPBaseModel):

    sender: str

    receiver: str

    message_type: str

    trace_id: str

    payload: dict[str, Any]
