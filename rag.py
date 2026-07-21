from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain

from llm import llm
from prompt import prompt_RAG


# ==========================
# Cargar documentos
# ==========================

ruta_pdfs = Path("./documentos")

docs = []

for archivo in ruta_pdfs.glob("*.pdf"):

    print(f"Cargando: {archivo.name}")

    loader = PyMuPDFLoader(str(archivo))
    docs.extend(loader.load())


# ==========================
# Dividir documentos
# ==========================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)


# ==========================
# Embeddings
# ==========================

embeddings = OllamaEmbeddings(
    model="bge-m3"
)


# ==========================
# Vector Store
# ==========================

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 3
    }
)


# ==========================
# Cadena RAG
# ==========================

document_chain = create_stuff_documents_chain(
    llm,
    prompt_RAG
)


# ==========================
# Función principal
# ==========================

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
