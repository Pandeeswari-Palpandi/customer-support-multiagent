import asyncio

from agents import router_agent


async def test_router(question: str):
    response = await router_agent.run(
        task=question
    )

    department = response.messages[-1].content.strip()

    print("\nCustomer Question:")
    print(question)

    print("\nRouted Department:")
    print(department)


async def main():

    questions = [
        "My laptop is not connecting to the company VPN.",
        "How many casual leaves can I take?",
        "When will my salary be credited?",
        "I need a new office ID card.",
        "Can you give me the price of your product?",
        "I need help reviewing a company contract.",
        "I have a general question about the company.",
    ]

    for question in questions:
        await test_router(question)


if __name__ == "__main__":
    asyncio.run(main())
