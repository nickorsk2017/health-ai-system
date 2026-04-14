from langgraph.graph import END, StateGraph

from nodes.fetch_all_data import fetch_history_labs
from nodes.run_consilium import run_consilium
from schemas.state import ConsiliumState


def build_consilium_chain() -> StateGraph:
    graph = StateGraph(ConsiliumState)

    graph.add_node("fetch_history_labs", fetch_history_labs)
    graph.add_node("run_consilium", run_consilium)

    graph.set_entry_point("fetch_history_labs")
    graph.add_edge("fetch_history_labs", "run_consilium")
    graph.add_edge("run_consilium", END)

    return graph.compile()
