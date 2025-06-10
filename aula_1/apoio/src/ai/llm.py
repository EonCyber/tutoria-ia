from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
load_dotenv()
class ChatBot:
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=None,
    timeout=None,)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um goblin servo, pronto para ajudar, fale com reverencia com seu mestre."),
            ("human", "{input}")
        ])
        self.chain = self.prompt | self.llm | StrOutputParser()

        
    def answer(self, input_message):
        return self.chain.invoke({'input': input_message})