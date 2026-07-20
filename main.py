from pathlib import Path
import os

from dotenv import load_dotenv

from typing import TypedDict, Optional, Literal, List

from pydantic import BaseModel, Field

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage

from langchain.chains.combine_documents import create_stuff_documents_chain

from langgraph.graph import StateGraph, START, END



load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=GEMINI_API_KEY
)



ruta_pdfs = Path("./documentos")

docs = []


for archivo in ruta_pdfs.glob("*.pdf"):

    print(f"Cargando: {archivo.name}")

    loader = PyMuPDFLoader(str(archivo))

    docs.extend(loader.load())


print(f"Paginas cargadas: {len(docs)}")



splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


chunks = splitter.split_documents(docs)


print(f"Chunks creados: {len(chunks)}")



embeddings = OllamaEmbeddings(
    model="bge-m3"
)


vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k":3
    }
)


print("Retriever listo")



prompt_RAG = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Sos un asistente de soporte de la ecommerce Victory.

            Responde únicamente usando la información del contexto.

            Si no existe información suficiente en los documentos,
            indicá que no encontraste esa información.

            Contexto:
            {context}
            """
        ),
        (
            "human",
            "{input}"
        )
    ]
)


document_chain = create_stuff_documents_chain(
    llm,
    prompt_RAG
)



def responder_RAG(pregunta):

    documentos = retriever.invoke(pregunta)


    if not documentos:

        return {
            "respuesta": "No encontré información relacionada.",
            "documentos_encontrados": False
        }


    respuesta = document_chain.invoke(
        {
            "input": pregunta,
            "context": documentos
        }
    )


    return {
        "respuesta": respuesta,
        "documentos_encontrados": True
    }





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

    campos_faltantes: List[str] = Field(
        default_factory=list
    )



PROMPT_TRIAJE = """
Sos un clasificador de soporte para Victory.

Analiza la consulta.

DECISION:

responder:
- preguntas frecuentes
- envíos
- devoluciones
- políticas
- información presente en documentos

pedir_info:
- faltan datos del pedido
- falta número de compra
- falta información del cliente

abrir_ticket:
- reclamos
- problemas de pago
- productos defectuosos
- problemas que requieren humano


URGENCIA:

baja:
consultas generales

media:
problemas con pedidos existentes

alta:
pagos incorrectos, fraude, pérdida de dinero


Siempre devolvé una decisión correcta.
"""


chain_triaje = llm.with_structured_output(
    TriajeOut
)


class AgentState(TypedDict, total=False):

    pregunta: str
    triaje: dict
    respuesta: Optional[str]
    rag_exito: bool
    accion_final: str





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

    resultado = responder_RAG(
        state["pregunta"]
    )


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




workflow = StateGraph(AgentState)


workflow.add_node(
    "triaje",
    nodo_triaje
)


workflow.add_node(
    "auto_resolver",
    nodo_auto_resolver
)


workflow.add_node(
    "pedir_info",
    nodo_pedir_info
)


workflow.add_node(
    "abrir_ticket",
    nodo_abrir_ticket
)



workflow.add_edge(
    START,
    "triaje"
)


workflow.add_conditional_edges(
    "triaje",
    decidir_siguiente
)



workflow.add_edge(
    "auto_resolver",
    END
)


workflow.add_edge(
    "pedir_info",
    END
)


workflow.add_edge(
    "abrir_ticket",
    END
)



app = workflow.compile()



resultado = app.invoke(
    {
        "pregunta": "Quiero devolver mi producto"
    }
)


print("\nRESULTADO FINAL")
print(resultado)