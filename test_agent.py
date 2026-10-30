import asyncio

from agents import it_agent


async def main():
    response = await it_agent.run(
        task="My laptop is connected to Wi-Fi, but I cannot connect to the company VPN."
    )

    print("\n--- IT AGENT RESPONSE ---\n")
    print(response.messages[-1].content)

if __name__ == "__main__":
    asyncio.run(main())
