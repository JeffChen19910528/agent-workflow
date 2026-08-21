import asyncio

from agent_workflow import Agent


async def demo() -> None:
    agent = Agent()
    test_input = "Cybersecurity systems detect malware and prevent attacks."

    result = await agent.run(test_input)

    print("Input:", test_input)
    print("Decision + Output:", result)


if __name__ == "__main__":
    asyncio.run(demo())
