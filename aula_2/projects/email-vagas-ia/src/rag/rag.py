from langchain_docling import DoclingLoader
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from util.stdout import logtext

EMBEDDING_MODEL_TYPE = 'text-embedding-3-large'
FAISS_STORE_PATH = 'src/db/cv_faiss_store'

class CVRetrieval:
    """
        CVRetrieval Class
        - This class is responsible for loading and managing the retrieval of CV documents.
        - It uses the DoclingLoader to load documents, OpenAIEmbeddings for embeddings, and FAISS for vector storage.
        - The class can create a retriever from existing FAISS vector store or create a new one if it does not exist.
        - It provides methods to load embeddings, create a retriever, and fetch the retriever.
        - The retriever can be used to retrieve relevant documents based on the input content.      
    """
    def __init__(self, path):
        self.document_path = path
        self.retriever = None

    def create_loader(self, path):
        return DoclingLoader(file_path=path)
    
    def load_embeddings(self):
        return OpenAIEmbeddings(model=EMBEDDING_MODEL_TYPE)
    
    def load_retriever(self):
        logtext("Carregando Embeddings...")
        embeddings = self.load_embeddings()
        if Path(FAISS_STORE_PATH).exists():
            """
            If the FAISS vector store already exists, load it from the local path.
            This allows for faster retrieval without needing to recreate the vector store.
            """
            logtext("Vector Database(FAISS) local encontrado!")
            logtext("Carregando Retriever a partir do vDB local...")
            faiss_index = FAISS.load_local(FAISS_STORE_PATH, embeddings, allow_dangerous_deserialization=True) 
            self.retriever = faiss_index.as_retriever()
            logtext("Retriever Carregado.")
        else:
            """
            If the FAISS vector store does not exist, create it from the documents.
            This involves loading the documents, splitting them into chunks, and creating a new FAISS vector store.
            The new vector store is then saved to the local path for future use.
            """
            logtext("Criando e salvando VectorStore...")
            docs = self.create_loader(self.document_path).load()
            splitter = RecursiveCharacterTextSplitter(
                            chunk_size=500,
                            chunk_overlap=0
                        )
            chunks = splitter.split_documents(docs)
            faiss_index = FAISS.from_documents(
                documents=chunks,
                embedding=embeddings
                )
            faiss_index.save_local(FAISS_STORE_PATH)
            self.retriever = faiss_index.as_retriever()
            logtext("Retriever Criado e Carregado.")
    
    def fetch_retriever(self):
        if self.retriever:
            return self.retriever
        else:
            raise Exception("Erro: Retriever nao encontrado.")