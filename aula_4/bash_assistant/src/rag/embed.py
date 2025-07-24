
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

# import os
load_dotenv()

EMBEDDING_MODEL_TYPE = "text-embedding-3-large"

def make_embeddings():
    """
    Função para criar embeddings usando o modelo especificado.
    Retorna um objeto de embeddings configurado.
    """
    # 1. Embeddings
    # embeds = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_TYPE)
    embeds = OpenAIEmbeddings(model=EMBEDDING_MODEL_TYPE)

    return embeds

def make_chunks():
    """
    Função para criar chunks de documentos Markdown.
    """
    # 1. Carregar documentos .md
    loader = DirectoryLoader("src/data", glob="**/*.md")
    docs = loader.load()

    # 2. Dividir em chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    chunks = splitter.split_documents(docs)

    return chunks