import pytest

from agent_workflow.agent import Agent
from agent_workflow.classifier import GENERAL, SECURITY, TextClassifier
from agent_workflow.summarizer import TextSummarizer


class FakeLLMClient:
    def __init__(self, response: str):
        self.response = response
        self.prompts = []

    async def generate_async(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


@pytest.mark.asyncio
async def test_classifier_detects_security_text():
    classifier = TextClassifier(FakeLLMClient("Security"))
    assert await classifier.classify("some text") == SECURITY


@pytest.mark.asyncio
async def test_classifier_defaults_to_general():
    classifier = TextClassifier(FakeLLMClient("general"))
    assert await classifier.classify("some text") == GENERAL


@pytest.mark.asyncio
async def test_summarizer_returns_llm_output():
    llm = FakeLLMClient("a short summary")
    summarizer = TextSummarizer(llm)
    result = await summarizer.summarize("long text")
    assert result == "a short summary"
    assert "long text" in llm.prompts[0]


@pytest.mark.asyncio
async def test_agent_routes_security_text_to_summary():
    classifier = TextClassifier(FakeLLMClient(SECURITY))
    summarizer = TextSummarizer(FakeLLMClient("summary result"))
    agent = Agent(classifier=classifier, summarizer=summarizer)

    result = await agent.run("malware detection systems")

    assert result == "[SECURITY SUMMARY]: summary result"


@pytest.mark.asyncio
async def test_agent_echoes_general_text():
    classifier = TextClassifier(FakeLLMClient(GENERAL))
    summarizer = TextSummarizer(FakeLLMClient("unused"))
    agent = Agent(classifier=classifier, summarizer=summarizer)

    result = await agent.run("what's the weather today")

    assert result == "[GENERAL RESPONSE]: what's the weather today"
