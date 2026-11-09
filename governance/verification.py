from pydantic import Field

from core.base import EGPBaseModel


class VerificationResult(EGPBaseModel):

    status: bool

    score: float = Field(
        ge=0.0,
        le=1.0
    )

    message: str | None = None

    evidence: list[str] = []


class VerificationCore(EGPBaseModel):

    consistency_check: VerificationResult

    topology_check: VerificationResult

    dependency_check: VerificationResult

    reference_check: VerificationResult

    drift_check: VerificationResult

    invariant_check: VerificationResult

    mask_integrity_check: VerificationResult
