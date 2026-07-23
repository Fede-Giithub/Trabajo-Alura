from pathlib import Path

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
import google.generativeai as genai
import os

from llm import llm
from prompt import prompt_RAG

from dotenv import load_dotenv
import os

load_dotenv()

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

from langchain_google_genai import GoogleGenerativeAIEmbeddings



genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GeminiEmbeddings:

    def embed_documents(self, texts):
        return [
            genai.embed_content(
                model="models/gemini-embedding-001",
                content=text,
                task_type="retrieval_document"
            )["embedding"]
            for text in texts
        ]

    def embed_query(self, text):
        return genai.embed_content(
            model="models/gemini-embedding-001",
            content=text,
            task_type="retrieval_query"
        )["embedding"]

    def __call__(self, text):
        return self.embed_query(text)

        
embeddings = GeminiEmbeddings()


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
