from src.config.llm import llm
from src.graph.state import SchedulerState
from src.prompts.triage_prompt import TRIAGE_PROMPT
from langchain_core.messages import HumanMessage,SystemMessage

class TriageAgent:
    def __init__(self):
        self.llm = llm

    def process(self, state: SchedulerState):
        user_input = state["user_input"]
        response = self.llm.invoke(
            [
                SystemMessage(content=TRIAGE_PROMPT),
                HumanMessage(content=user_input),
            ]
        )
        intent = response.content.strip().lower()
        state["intent"] = intent
        if intent == "greeting":
            state["response"] = (
                "Hello! How can I help you schedule an appointment today?"
            )
        elif intent == "unknown":
            state["response"] = (
                "I can help you book appointments or check availability."
            )
        return state