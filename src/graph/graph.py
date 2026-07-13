import sqlite3

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph

from src.agents.booking_agent import BookingAgent
from src.agents.triage_agent import TriageAgent
from src.graph.state import SchedulerState


triage_agent = TriageAgent()
booking_agent = BookingAgent()

graph = StateGraph(SchedulerState)

graph.add_node("triage", triage_agent.process)
graph.add_node("booking", booking_agent.process)

graph.add_edge(START, "triage")


def route_booking(state: SchedulerState):

    if state.get("booking_status") == "pending":
        return "booking"

    if state["intent"] in ("booking", "availability"):
        return "booking"

    return END


graph.add_conditional_edges("triage", route_booking)

graph.add_edge("booking", END)


connection = sqlite3.connect(
    "graph_memory.db",
    check_same_thread=False,
)

checkpointer = SqliteSaver(connection)

scheduler_graph = graph.compile(
    checkpointer=checkpointer
)