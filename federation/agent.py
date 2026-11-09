from core.base import EGPBaseModel


class AgentDescriptor(EGPBaseModel):

    agent_id: str

    agent_type: str

    capabilities: list[str]

    required_policies: list[str]

    required_verifications: list[str]
