from rag.embed import make_embeddings, make_chunks
from rag.faiss_rag import make_faiss_retriever, make_faiss_index_reranker_retriever
from tools.make_tools import make_tldr_simple_rag_tool, make_tldr_reranker_rag_tool
from agent.bash_assistant import create_agent, invoke

# 1. Criar embeddings
embeds = make_embeddings()

# 2. Criar chunks de documentos
chunks = make_chunks()

# 3. Criar retriever simples
# simple_retriever = make_faiss_retriever(chunks, embeds)

# 4. Criar retriever com re-ranker
reranker_retriever = make_faiss_index_reranker_retriever(chunks, embeds)

# 5. Criar ferramentas
# simple_tool = make_tldr_simple_rag_tool(simple_retriever)
reranker_tool = make_tldr_reranker_rag_tool(reranker_retriever)

# 6. Criar agente
tools = [reranker_tool]  # Adicione simple_tool se necessário
agent = create_agent(tools)

if __name__ == "__main__":
    # 7. Invocar agente com uma consulta de exemplo
    query = "Como mostrar arquivos ocultos no terminal?"
    response = invoke(agent, query)

    print(query)
    print(response)