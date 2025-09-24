from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from ai.prompts.system import SYSTEM_PROMPT
from langgraph.graph import MessagesState, StateGraph, START, END
from dotenv import load_dotenv
import uuid

load_dotenv()

def memory_node(state: MessagesState, config: RunnableConfig, *, store):
    user_id = config["configurable"].get("user_id", "anon")
    namespace = (user_id, "memories")
    # Recupera memórias semelhantes
    memories = store.search(namespace, query=state["messages"][-1].content, limit=2)
    memory_text = "\n".join([m.value["content"] for m in memories])
    state["memory_context"] = memory_text  # adiciona contexto de memória ao estado
    # Armazena a nova informação
    mem_id = str(uuid.uuid4())
    store.put(namespace, mem_id, {"content": state["messages"][-1].content})
    return state


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