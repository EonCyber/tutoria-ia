from langchain_docling import DoclingLoader
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from util.stdout import logtext
EMBEDDING_MODEL_TYPE = 'text-embedding-3-large'
FAISS_STORE_PATH = 'src/db/cv_faiss_store'

class CVRetrieval:
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

            """
            logtext("Vector Database(FAISS) local encontrado!")
            logtext("Carregando Retriever a partir do vDB local...")
            faiss_index = FAISS.load_local(FAISS_STORE_PATH, embeddings, allow_dangerous_deserialization=True) 
            self.retriever = faiss_index.as_retriever()
            logtext("Retriever Carregado.")
        else:
            logtext("Criando e salvando VectorStore...")
            docs = self.create_loader(self.document_path).load()
            splitter = RecursiveCharacterTextSplitter(
                            chunk_size=500,
                            chunk_overlap=0
                        )
            chunks = splitter.split_documents(docs)
            faiss_index = FAISS.from_documents(documents=chunks, embedding=embeddings)
            faiss_index.save_local(FAISS_STORE_PATH)
            self.retriever = faiss_index.as_retriever()
            logtext("Retriever Criado e Carregado.")
    
    def fetch_retriever(self):
        if self.retriever:
            return self.retriever
        else:
            raise Exception("Erro: Retriever nao encontrado.")