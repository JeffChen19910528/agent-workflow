from .classifier import SECURITY, TextClassifier
from .config import Config
from .llm_client import LLMClient
from .summarizer import TextSummarizer


class Agent:
    """Routes input text to a summarizer when it's security-related, otherwise echoes it back."""

    def __init__(
        self,
        name: str = "LLM Agent",
        classifier: TextClassifier | None = None,
        summarizer: TextSummarizer | None = None,
        config: Config | None = None,
    ):
        self.name = name
        llm_client = LLMClient(config)
        self.classifier = classifier or TextClassifier(llm_client)
        self.summarizer = summarizer or TextSummarizer(llm_client)

    async def run(self, input_text: str) -> str:
        decision = await self.classifier.classify(input_text)

        if decision == SECURITY:
            result = await self.summarizer.summarize(input_text)
            return f"[SECURITY SUMMARY]: {result}"
        return f"[GENERAL RESPONSE]: {input_text}"
