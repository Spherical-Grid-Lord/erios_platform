from core.base import EGPBaseModel


class TraceContext(EGPBaseModel):

    trace_id: str

    span_id: str

    parent_span_id: str | None = None

    workflow_id: str
