from pydantic import Field

from core.base import AuditMixin
from core.enums import TreeStatus


class TreeState(AuditMixin):

    trunk: str = Field(min_length=1)

    branch: str = Field(min_length=1)

    leaf: str = Field(min_length=1)

    status: TreeStatus = TreeStatus.ACTIVE
