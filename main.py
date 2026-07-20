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