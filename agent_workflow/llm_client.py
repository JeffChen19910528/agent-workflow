import asyncio

import requests

from .config import Config


class LLMError(RuntimeError):
    """Raised when the LLM backend cannot be reached or returns an unusable response."""


class LLMClient:
    """Thin synchronous/async wrapper around an Ollama-compatible generate endpoint."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config.from_env()

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.config.base_url}/api/generate",
                json={
                    "model": self.config.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=self.config.timeout,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise LLMError(f"failed to reach LLM backend: {exc}") from exc

        try:
            return response.json()["response"]
        except (ValueError, KeyError) as exc:
            raise LLMError(f"unexpected LLM response payload: {exc}") from exc

    async def generate_async(self, prompt: str) -> str:
        return await asyncio.to_thread(self.generate, prompt)
