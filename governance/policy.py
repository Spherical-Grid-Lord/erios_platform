from core.base import EGPBaseModel


class Policy(EGPBaseModel):

    policy_id: str

    non_destructive: bool = True

    repository_first: bool = True

    verification_required: bool = True

    allow_external_search: bool = False

    allow_route_c_direct_promotion: bool = False

    minimum_fruit_level: str = "F3"
