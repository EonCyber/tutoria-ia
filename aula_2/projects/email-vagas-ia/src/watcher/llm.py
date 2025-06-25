from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableMap
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.variables import EMAIL_ANALYSIS_PROMPT


GPT_MODEL = 'gpt-4o-mini'

class RagContextChain:
    """
    RAG Context Chain for Email Analysis using LLM
    - This is a class that uses LangChain to create a context-aware RAG (Retrieval-Augmented Generation) chain for email analysis.
    - It retrieves relevant documents based on the input content and generates a response using a language model.
    """
    def __init__(self, retriever):
        self.retriever = retriever
        self.prompt = ChatPromptTemplate.from_template(EMAIL_ANALYSIS_PROMPT)
        self.llm =  ChatOpenAI(model=GPT_MODEL, temperature=0.1)

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def answer(self, content):
        return (
            RunnableMap({
                "context": self.retriever | self.format_docs,
                "input": RunnablePassthrough()
            })
            | self.prompt 
            | self.llm
            | StrOutputParser()
        ).invoke(content)