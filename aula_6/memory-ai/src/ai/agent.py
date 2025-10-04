from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ai.prompts.system import SYSTEM_PROMPT
from langgraph.graph import MessagesState, StateGraph, START, END
from dotenv import load_dotenv
import uuid

load_dotenv()

def make_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

def extract_ai_answer(final_state):
    return final_state['messages'][-1].content

def input_with_state(input: str):
    return { 'messages': [HumanMessage(content=input)]}

def make_agentic_node(llm: ChatOpenAI):
    def assistent(state: MessagesState):
        system_message = SystemMessage(content=SYSTEM_PROMPT)
        messages = [system_message] + state["messages"]
        response = llm.invoke(messages)
        return {"messages": messages + [response]}
    return assistent 

def build_graph():
    llm = make_llm()   
    agent = make_agentic_node(llm) 
    builder = StateGraph(MessagesState)
    builder.add_node('agent', agent)
    builder.add_edge(START, 'agent')
    builder.add_edge('agent', END)
    return builder.compile()