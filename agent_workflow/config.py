import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    base_url: str = "http://localhost:11434"
    model: str = "gemma4"
    timeout: float = 30.0

    @classmethod
    def from_env(cls) -> "Config":
        return cls(
            base_url=os.environ.get("AGENT_LLM_BASE_URL", cls.base_url),
            model=os.environ.get("AGENT_LLM_MODEL", cls.model),
            timeout=float(os.environ.get("AGENT_LLM_TIMEOUT", cls.timeout)),
        )
