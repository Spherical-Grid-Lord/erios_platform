from core.base import AuditMixin
from core.enums import FruitLevel


class Fruit(AuditMixin):

    fruit_id: str

    title: str

    level: FruitLevel

    verified: bool = False

    owner: str | None = None
