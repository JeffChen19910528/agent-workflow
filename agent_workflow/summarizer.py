from .llm_client import LLMClient


class TextSummarizer:
    """Summarizes text using an LLM."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def summarize(self, text: str) -> str:
        prompt = f"Summarize this text:\n{text}"
        return await self.llm_client.generate_async(prompt)
