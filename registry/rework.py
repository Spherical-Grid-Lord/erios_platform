from core.base import AuditMixin
from core.enums import ReworkStatus


class ReworkRecord(AuditMixin):

    rework_id: str

    target_branch: str

    failure: str

    root_cause: str

    resolution: str

    prevention: str

    status: ReworkStatus
