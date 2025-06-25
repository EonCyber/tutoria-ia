from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.sql_database import SQLDatabase
from operator import itemgetter
class SQLChain:

    def __init__(self, prompt, llm):
        self.llm = llm
        self.prompt = prompt
    
    def chain(self):
        return (
            {
                'schema': itemgetter('schema'),
                'question': itemgetter('schema')
            }
            | self.prompt
            | self.llm.bind(stop='\nSQL Query:')
            | StrOutputParser()
        )