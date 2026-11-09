from core.base import EGPBaseModel
from governance.tree_state import TreeState
from governance.layer import LayerClassification
from governance.route import RouteClassification
from governance.policy import Policy
from governance.provenance import Provenance
from governance.verification import VerificationCore
from telemetry.trace import TraceContext


class EGPEnvelope(EGPBaseModel):

    protocol_name: str = "EGP"

    protocol_version: str = "2.0"

    trace: TraceContext

    policy: Policy

    tree_state: TreeState

    layers: LayerClassification

    routes: RouteClassification

    provenance: Provenance

    verification: VerificationCore
