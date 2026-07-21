from langgraph.graph import StateGraph, START, END

from lang import (
    AgentState,
    nodo_triaje,
    nodo_auto_resolver,
    nodo_pedir_info,
    nodo_abrir_ticket,
    decidir_siguiente
)

workflow = StateGraph(AgentState)

workflow.add_node("triaje", nodo_triaje)
workflow.add_node("auto_resolver", nodo_auto_resolver)
workflow.add_node("pedir_info", nodo_pedir_info)
workflow.add_node("abrir_ticket", nodo_abrir_ticket)

workflow.add_edge(START, "triaje")

workflow.add_conditional_edges(
    "triaje",
    decidir_siguiente
)

workflow.add_edge("auto_resolver", END)
workflow.add_edge("pedir_info", END)
workflow.add_edge("abrir_ticket", END)

app = workflow.compile()