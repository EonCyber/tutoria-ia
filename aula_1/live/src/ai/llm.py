from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()

class ChatBot:
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, timeout=None)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um Goblin servo pronto para ajudar, fale com reverencia com seu mestre. Extraia informaçao do texto e crie um json de resposta."),
            ("human", "{input}")
        ])
        # CHAIN 
        self.chain = self.prompt | self.llm | StrOutputParser()

    def answer(self, input_message):
        return self.chain.invoke({ 'input': input_message })