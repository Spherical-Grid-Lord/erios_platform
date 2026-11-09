from governance.tree_state import TreeState
from governance.route import RouteClassification
from governance.layer import LayerClassification
from governance.verification import VerificationCore
from registry.fruit import Fruit
from core.base import EGPBaseModel


class RuntimeState(EGPBaseModel):

    workflow_id: str

    tree_state: TreeState

    layers: LayerClassification

    routes: RouteClassification

    verification: VerificationCore | None = None

    fruit: Fruit | None = None
