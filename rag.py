from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain

from llm import llm
from prompt import prompt_RAG



ruta_pdfs = Path("./documentos")

docs = []

for archivo in ruta_pdfs.glob("*.pdf"):

    print(f"Cargando: {archivo.name}")

    loader = PyMuPDFLoader(str(archivo))
    docs.extend(loader.load())



splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",
    model_kwargs={"device": "cpu"}
)



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
