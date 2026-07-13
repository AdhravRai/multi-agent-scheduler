from langgraph.graph import StateGraph, START, END
from src.agents.booking_agent import BookingAgent
from src.agents.triage_agent import TriageAgent
from src.graph.state import SchedulerState
from langgraph.checkpoint.sqlite import SqliteSaver

triage_agent = TriageAgent()
booking_agent = BookingAgent()
graph = StateGraph(SchedulerState)
graph.add_node("triage",triage_agent.process,)
graph.add_node("booking",booking_agent.process,)
graph.add_edge(START,"triage",)

def route_booking(state: SchedulerState):
    if state["intent"] in ("booking", "availability"):
        return "booking"

    return END
graph.add_conditional_edges("triage",route_booking)
graph.add_edge("booking",END,)
connection = sqlite3.connect(
    "graph_memory.db",
    check_same_thread=False,
)
checkpointer = SqliteSaver(connection)
scheduler_graph = graph.compile(checkpointer=checkpointer)