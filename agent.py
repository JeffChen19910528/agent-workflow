import asyncio
import requests

class Agent:
    def __init__(self):
        self.name = "LLM Agent"
        self.model = "gemma4"

    def call_llm(self, prompt):
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
        )
        return response.json()["response"]

    async def analyze(self, text):
        prompt = f"""
        Determine if the following text is related to cybersecurity.
        Answer only "security" or "general".

        Text: {text}
        """
        result = self.call_llm(prompt)
        return result.strip().lower()

    async def summarize(self, text):
        prompt = f"Summarize this text:\n{text}"
        return self.call_llm(prompt)

    async def run(self, input_text):
        decision = await self.analyze(input_text)

        if "security" in decision:
            result = await self.summarize(input_text)
            return f"[SECURITY SUMMARY]: {result}"
        else:
            return f"[GENERAL RESPONSE]: {input_text}"


# 測試
if __name__ == "__main__":
    agent = Agent()

    test_input = "Cybersecurity systems detect malware and prevent attacks."

    result = asyncio.run(agent.run(test_input))

    print("Input:", test_input)
    print("Decision + Output:", result)