from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.callbacks.base import BaseCallbackHandler
from ai.sql_chain import SQLChain
from ai.natural_chain import NaturalChain
from prompts.variables import NATURAL_RESPONSE_TEMPLATE,SQL_CHAIN_TEMPLATE
LLM_MODEL = 'gpt-4o-mini'
class SQLPrinter(BaseCallbackHandler):
    def on_llm_end(self, response, **kwargs):
        # The generated SQL will be in response.generations if single
        text = response.generations[0][0].text.strip()
        print("\n🔍 Chain Response:", text)
class AiService:

    def __init__(self, engine):
        self.llm = ChatOpenAI(model=LLM_MODEL, temperature=0.3)
        self.db = SQLDatabase(engine)
        self.sql_chain = SQLChain(ChatPromptTemplate.from_template(SQL_CHAIN_TEMPLATE), self.llm).chain()
        self.chain = NaturalChain(ChatPromptTemplate.from_template(NATURAL_RESPONSE_TEMPLATE), self.llm, self.db, self.sql_chain).chain()

    def answer(self, input_question):
        return self.chain.invoke(
                    {"question": input_question},
                    {"callbacks": [SQLPrinter()]}
                )