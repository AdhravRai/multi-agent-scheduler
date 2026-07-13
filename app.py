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
        "messages": st.session_state.messages,
        "user_input": user_input,
        "intent": "",
        "date": "",
        "time": "",
        "email": "",
        "missing_fields": [],
        "booking_status": "",
        "response": "",
    }

    config = {
        "configurable": {
            "thread_id": "default-user"
        }
    }
    
    result = scheduler_graph.invoke(
        state,
        config=config,
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