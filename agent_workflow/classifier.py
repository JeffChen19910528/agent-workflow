from .llm_client import LLMClient

SECURITY = "security"
GENERAL = "general"

_PROMPT_TEMPLATE = """\
Determine if the following text is related to cybersecurity.
Answer only "security" or "general".

Text: {text}
"""


class TextClassifier:
    """Classifies text as security-related or general using an LLM."""

    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client

    async def classify(self, text: str) -> str:
        prompt = _PROMPT_TEMPLATE.format(text=text)
        result = await self.llm_client.generate_async(prompt)
        return SECURITY if SECURITY in result.strip().lower() else GENERAL
