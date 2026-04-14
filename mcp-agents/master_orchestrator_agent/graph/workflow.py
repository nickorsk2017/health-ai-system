from langgraph.graph import END, StateGraph

from graph.nodes import gather_data, run_consilium
from graph.state import OrchestratorState


def build_workflow() -> StateGraph:
    graph = StateGraph(OrchestratorState)

    graph.add_node("gather_data", gather_data)
    graph.add_node("run_consilium", run_consilium)

    graph.set_entry_point("gather_data")
    graph.add_edge("gather_data", "run_consilium")
    graph.add_edge("run_consilium", END)

    return graph.compile()
