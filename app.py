import uuid

import streamlit as st

from src.graph.graph import scheduler_graph


st.set_page_config(
    page_title="Multi-Agent Scheduler",
    page_icon="📅",
    layout="centered",
)

st.title("📅 Multi-Agent Scheduling Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_input = st.chat_input("Type your message...")


if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    state = {
        "messages": [
            {
                "role": "user",
                "content": user_input,
            }
        ],
        "user_input": user_input,
    }

    result = scheduler_graph.invoke(
        state,
        config={
            "configurable": {
                "thread_id": st.session_state.thread_id,
            }
        },
    )

    response = result["response"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

    with st.chat_message("assistant"):
        st.markdown(response)