from langgraph.graph import END, StateGraph

from nodes.fetch_all_data import fetch_all_data
from nodes.run_consilium import run_consilium
from nodes.run_gp_synthesis import run_gp_synthesis
from schemas.state import GPDiagnosisState


def build_gp_diagnosis_chain() -> StateGraph:
    graph = StateGraph(GPDiagnosisState)

    graph.add_node("fetch_all_data", fetch_all_data)
    graph.add_node("run_consilium", run_consilium)
    graph.add_node("run_gp_synthesis", run_gp_synthesis)

    graph.set_entry_point("fetch_all_data")
    graph.add_edge("fetch_all_data", "run_consilium")
    graph.add_edge("run_consilium", "run_gp_synthesis")
    graph.add_edge("run_gp_synthesis", END)

    return graph.compile()
