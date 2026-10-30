import asyncio
import threading
from concurrent.futures import Future

from agents import (
    router_agent,
    department_agents,
)

OUT_OF_SCOPE_RESPONSE = (
    "I can help with company support questions about IT, HR, Finance, "
    "Administration, Sales, or Legal. Please ask about one of these topics."
)

_response_loop: asyncio.AbstractEventLoop | None = None
_response_loop_lock = threading.Lock()


def _build_contextual_task(
    question: str,
    conversation_history: list[dict[str, str]],
) -> str:
    if not conversation_history:
        return question

    history = "\n".join(
        f"{'Customer' if message['role'] == 'user' else 'Support'}: "
        f"{message['content']}"
        for message in conversation_history
        if message["role"] in {"user", "assistant"}
    )

    if not history:
        return question

    return (
        "Conversation history (oldest first):\n"
        f"{history}\n\n"
        "Latest customer message (respond to this message):\n"
        f"{question}"
    )


async def handle_customer_question(
    question: str,
    conversation_history: list[dict[str, str]] | None = None,
):
    """
    Routes a customer question and answers it using prior conversation context.
    """
    contextual_task = _build_contextual_task(
        question,
        conversation_history or [],
    )

    # -----------------------------------------------------
    # Step 1: Ask Router Agent to identify department
    # -----------------------------------------------------

    router_response = await router_agent.run(
        task=contextual_task
    )

    department = router_response.messages[-1].content.strip().upper()

    # -----------------------------------------------------
    # Step 2: Keep unrelated requests out of department agents
    # -----------------------------------------------------

    if department not in department_agents:
        department = "OUT_OF_SCOPE"

    if department == "OUT_OF_SCOPE":
        return {
            "department": department,
            "answer": OUT_OF_SCOPE_RESPONSE,
        }

    # -----------------------------------------------------
    # Step 3: Get the correct department agent
    # -----------------------------------------------------

    selected_agent = department_agents[department]

    # -----------------------------------------------------
    # Step 4: Ask department agent to answer
    # -----------------------------------------------------

    department_response = await selected_agent.run(
        task=contextual_task
    )

    answer = department_response.messages[-1].content.strip()

    # -----------------------------------------------------
    # Step 5: Return routing information + answer
    # -----------------------------------------------------

    return {
        "department": department,
        "answer": answer,
    }


def handle_customer_question_sync(
    question: str,
    conversation_history: list[dict[str, str]] | None = None,
) -> dict[str, str]:
    """Run a support request on a persistent loop for synchronous UI callers."""
    global _response_loop

    with _response_loop_lock:
        if _response_loop is None or _response_loop.is_closed():
            _response_loop = asyncio.new_event_loop()
            loop_thread = threading.Thread(
                target=_response_loop.run_forever,
                name="customer-support-async-loop",
                daemon=True,
            )
            loop_thread.start()
        response_loop = _response_loop

    future: Future[dict[str, str]] = asyncio.run_coroutine_threadsafe(
        handle_customer_question(question, conversation_history),
        response_loop,
    )
    return future.result()


# ---------------------------------------------------------
# Test the complete customer support workflow
# ---------------------------------------------------------

async def main():

    questions = [
        "My laptop is connected to Wi-Fi but VPN is not working.",
        "How many casual leaves can I take?",
        "When will my reimbursement be processed?",
        "I lost my office ID card.",
        "Can you tell me the pricing of your product?",
        "I need help with a company contract.",
    ]

    for question in questions:

        print("\n" + "=" * 60)

        print("CUSTOMER:")
        print(question)

        result = await handle_customer_question(question)

        print("\nROUTED TO:")
        print(result["department"])

        print("\nRESPONSE:")
        print(result["answer"])

        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
