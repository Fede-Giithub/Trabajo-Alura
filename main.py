!pip install -q langchain
!pip install -q langchain-community
!pip install -q langchain-google-genai
!pip install -q faiss-cpu
!pip install -q pymupdf



from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_google_genai import (ChatGoogleGenerativeAI,GoogleGenerativeAIEmbeddings)

from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain


llm= ChatGoogleGenerativeAI(
    model="",
    temperature=0,
    googleApiKey=GEMINI_API_KEY
)


class TriajeOut(model):
    decision: Literal[]
    urgencia:Literal[]
    campos_faltantes: List[str] = Field(default_factory=list)


chain_de_triaje= llm.with_structured_output(TriajeOut)

def triaje(mensaje: str) -> Dict:
    salida: TriajeOut=chain_de_triaje.invoke(
        [
            SystemMessage(content=PROMPT_TRIAJE),
            HumanMessage(content= mensaje)
        ]
    )
    return salida.model_dump()

for pregunta in mensaje_de_prueba





docs=[]

for n in Path("/content/").glob("*.pdf"):
    try:
        loader= PyMuPDFLoader(str(n))
        docs.extend(loader.load())
        print(f"Archivo cargado: {n.name}")
    except Exception as e:
        print(f"Error cargando archivo: {n.name}: {e}")



splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=20)
docs_splits = splitter.split_documents(docs)

modelo_embeddings=ChatGoogleGenerativeAIEmbeddings(
    model=""
    googleApiKey=GEMINI_API_KEY
)



vectostore=FAISS.from_documents(chunks,modelo_embeddings)

retriever = vectostore.as_retriever(
    search_type= "similarity"
    search_kwargs={""}
)

prompt_rag= ChatPromptTemplate(
    [
        ("""
        """)
    ]
)

document_chain =create_stuff(llm,prompt_rag)

def busqueda_de_respuestas_RAG(pregunta) -> Dict:
    documentos_relacionados= retriever.invoke(pregunta)
    if not documentos_relacionados:
    {
        "respuesta":"Nolo se",
        "citaciones" [],
        "documentos_encontrados":False
    }

    document_chain.invoke({
        "input":pregunta,
        "context":documentos_relacionados
    })

    if answer:


for pregunta in mensaje_de_prueba:
    respuesta_RAG=busqueda_de_respuestas_RAG(pregunta)
    if respuesta_RAG["documentos_Encontrados"]:
        for i, citacion in enumerate(respuesta_RAG["citaciones"])




class AgentState(TypedDict, total=False):
    pregunta:str
    triaje: dict
    respuesta: Optional[str]
    citaciones: Optional[str]
    rag_exito: bool
    accion_final: str



workflow = StateGraph(AgentState)

workflow.add_node("triaje",nodo_triaje)
workflow.add_node("auto_resolver",nodo_auto_resolver)
workflow.add_node("pedir_info",nodo_pedir_info)
workflow.add_node("abrir_ticket",nodo_abrir_ticket)

workflow.add_edge(START,"triaje")
workflow.add_conditional_edges("triaje")