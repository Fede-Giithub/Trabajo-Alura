from typing import TypedDict, Optional, Literal, List

from pydantic import BaseModel, Field

from langchain_core.messages import SystemMessage, HumanMessage

from llm import llm
from rag import responder_RAG
from prompt import PROMPT_TRIAJE


class AgentState(TypedDict, total=False):
    pregunta: str
    triaje: dict
    respuesta: Optional[str]
    rag_exito: bool
    accion_final: str


class TriajeOut(BaseModel):

    decision: Literal[
        "responder",
        "pedir_info",
        "abrir_ticket"
    ]

    urgencia: Literal[
        "baja",
        "media",
        "alta"
    ]

    campos_faltantes: List[str] = Field(default_factory=list)


chain_triaje = llm.with_structured_output(
    TriajeOut
)


def nodo_triaje(state: AgentState):

    salida = chain_triaje.invoke(
        [
            SystemMessage(content=PROMPT_TRIAJE),
            HumanMessage(content=state["pregunta"])
        ]
    )

    return {
        "triaje": salida.model_dump()
    }


def nodo_auto_resolver(state: AgentState):

    resultado = responder_RAG(state["pregunta"])

    return {
        "respuesta": resultado["respuesta"],
        "rag_exito": resultado["documentos_encontrados"],
        "accion_final": "respuesta_generada"
    }


def nodo_pedir_info(state: AgentState):

    return {
        "respuesta": "Necesito más información para ayudarte.",
        "accion_final": "pedir_informacion"
    }


def nodo_abrir_ticket(state: AgentState):

    return {
        "respuesta": "Se generó un ticket de soporte.",
        "accion_final": "ticket_creado"
    }


def decidir_siguiente(state: AgentState):

    decision = state["triaje"]["decision"]

    if decision == "responder":
        return "auto_resolver"

    elif decision == "pedir_info":
        return "pedir_info"

    else:
        return "abrir_ticket"