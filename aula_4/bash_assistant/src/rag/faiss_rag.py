from langchain_community.vectorstores import FAISS
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.cross_encoder_rerank import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

def make_faiss_retriever(chunks, embeds):
    """
    Função para criar um índice FAISS a partir de chunks e embeddings.
    Retorna o índice FAISS configurado.
    """
    faiss_index = None
    if Path("src/rag/faiss_simple").exists():
        # Carrega o índice FAISS existente
        faiss_index = FAISS.load_local("src/rag/faiss_simple", embeds, allow_dangerous_deserialization=True)
    else:
        # 1. Criar o índice FAISS
        faiss_index = FAISS.from_documents(chunks, embeds)

        # 2. Salvar o índice localmente
        faiss_index.save_local("src/rag/faiss_simple")

    return faiss_index.as_retriever(kwargs={"search_type": "similarity", "search_kwargs": {"k": 10}})

def make_faiss_index_reranker_retriever(chunks, embeds):
    """
    Função para criar um índice FAISS com re-ranker a partir de chunks e embeddings.
    Retorna o índice FAISS configurado com re-ranker.
    """
    # 1. FAISS + Reranker (RAG com re-rank)

    

    # Adiciona reranker (cross-encoder)
    hf_model  = HuggingFaceCrossEncoder(
        model_name="BAAI/bge-reranker-base",
        model_kwargs={"device": "cpu"}  # Use "cuda" if you have a GPU available
    )
    # Compressor/ reranker
    compressor = CrossEncoderReranker(model=hf_model, top_n=5)

    faiss_index = None
    if Path("src/rag/faiss_rerank").exists():
        # Carrega o índice FAISS existente
        faiss_index = FAISS.load_local("src/rag/faiss_rerank", embeds, allow_dangerous_deserialization=True)
    else:
        # Criar index com os dados
        faiss_index = FAISS.from_documents(chunks, embeds)
        faiss_index.save_local("src/rag/faiss_rerank")

     # Retriever vetorial base (por exemplo, FAISS)
    dense_retriever = faiss_index.as_retriever(kwargs={"search_type": "similarity", "search_kwargs": {"k": 10}})
    # Retorna o retriever com compressor
    return ContextualCompressionRetriever(
        base_retriever=dense_retriever,
        base_compressor=compressor
    )