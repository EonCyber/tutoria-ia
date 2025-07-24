from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class QueryArgs(BaseModel):
    query: str = Field(query=str, description="""
            Pergunta para buscar no TLDR dataset.
        """)

def make_tldr_simple_rag_tool(retriever):
    @tool(args_schema=QueryArgs, return_direct=True)
    def basic_command_helper(query: str) -> str:
        """
            Use esta ferramenta quando quiser encontrar rapidamente 
            um exemplo de uso de um comando de terminal (Bash/Linux).
        """
        docs = retriever.invoke(query)

        return "\n\n".join(doc.page_content for doc in docs)
    
    return basic_command_helper 

def make_tldr_reranker_rag_tool(re_retriever):
    @tool(args_schema=QueryArgs, return_direct=True)
    def reranker_command_helper(query):
        """
            Use esta ferramenta quando precisar de um exemplo 
            de comandos de terminal linux com consultas 
            mais relevante ou quando a consulta for ambígua (Bash/Linux).
        """
        docs = re_retriever.invoke(query)
        # doc.metadata["source"]
        return "\n\n".join(doc.page_content for doc in docs)
    return reranker_command_helper  