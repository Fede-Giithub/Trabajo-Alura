from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from pathlib import Path
import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyMuPDFLoader


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

    documentos = loader.load()

    docs.extend(documentos)


print(f"Cantidad de páginas cargadas: {len(docs)}")

from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


chunks = splitter.split_documents(docs)


print(f"Cantidad de chunks creados: {len(chunks)}")

from langchain_ollama import OllamaEmbeddings


embeddings = OllamaEmbeddings(
    model="bge-m3"
)

print("Modelo de embeddings cargado correctamente")

from langchain_community.vectorstores import FAISS


vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


print("FAISS creado correctamente")

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k":3
    }
)


print("Retriever listo")

pregunta = "¿Cuánto tarda un envío?"


documentos_encontrados = retriever.invoke(pregunta)


print("\n--- DOCUMENTOS ENCONTRADOS ---")

for i, doc in enumerate(documentos_encontrados):
    print(f"\nDocumento {i+1}")
    print(doc.page_content[:500])

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

prompt_RAG= ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
           

            Sos un asistente de soporte de una ecommerce llamada Victory. 
            Responde usando unicamente la información del contexto. Si la respuesta no está en los documentos, debes avisar que no encontraste esa información

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


documento_chain = create_stuff_documents_chain(
    llm,
    prompt_RAG
)

def responder_RAG(pregunta):

    documentos = retriever.invoke(pregunta)

    if not documentos:
        return {
            "respuesta": "No encontré información relacionada en los documentos.",
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


pregunta = "¿Cuánto tarda un envío?"

respuesta = responder_RAG(pregunta)

print("\n--- RESPUESTA ---")
print(respuesta)



from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    pregunta: str
    triaje: dict
    respuesta: Optional[str]
    rag_exito: bool
    accion_final: str



def nodo_auto_resolver(state: AgentState):

    pregunta = state["pregunta"]

    resultado = responder_RAG(pregunta)

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


workflow = StateGraph(AgentState)


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
    "auto_resolver"
)

workflow.add_edge(
    "auto_resolver",
    END
)


app = workflow.compile()