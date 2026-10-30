import importlib

import streamlit as st

import support_system

if not callable(getattr(support_system, "handle_customer_question_sync", None)):
    support_system = importlib.reload(support_system)

handle_customer_question_sync = support_system.handle_customer_question_sync


st.set_page_config(
    page_title="Customer Support Chat",
    page_icon="🎧",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f8fa;
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    [data-testid="stMainBlockContainer"] {
        max-width: 860px;
        padding-top: 2rem;
        padding-bottom: 6rem;
    }

    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎧 Customer Support")
st.caption("Ask a question, share details, and follow up naturally.")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Your conversation")
    st.caption("Chat with our support team.")
    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🎧"):
        st.markdown(
            "Hi! I’m here to help. What can I assist you with today?"
        )

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(message["content"])
        continue

    with st.chat_message("assistant", avatar="🎧"):
        department = message.get("department")
        if department and department != "OUT_OF_SCOPE":
            st.caption(f"Connected with {department} support")
        elif department == "OUT_OF_SCOPE":
            st.caption("Customer support")
        st.markdown(message["content"])

user_question = st.chat_input("Message customer support...")

if user_question:
    conversation_history = list(st.session_state.messages)
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question,
        }
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_question)

    with st.chat_message("assistant", avatar="🎧"):
        with st.spinner("Connecting you with the right support team..."):
            try:
                result = handle_customer_question_sync(
                    user_question,
                    conversation_history=conversation_history,
                )
                department = result["department"]
                answer = result["answer"]
                if department == "OUT_OF_SCOPE":
                    st.caption("Customer support")
                else:
                    st.caption(f"Connected with {department} support")
                st.markdown(answer)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "department": department,
                    }
                )
            except Exception as error:
                st.error(f"Unable to get a response: {error}")
