from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from agent.prompt import SYSTEM_PROMPT
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode
from dotenv import load_dotenv

load_dotenv()
agent_memory = MemorySaver()
system_msg = SystemMessage(content=SYSTEM_PROMPT)

def make_llm_with_tools(tools):
    print('Inicializando OpenAi LLM com Ferramentas...')
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2,
    ).bind_tools(tools)

def make_assistent_node(llm: ChatOpenAI):
    def assistent(state: MessagesState):
        messages = state['messages']
        response = llm.invoke(messages)
        return {"messages": messages + [response]}
    return assistent

def build_graph(tools):
    llm = make_llm_with_tools(tools)
    assistant_node = make_assistent_node(llm)

    builder = StateGraph(MessagesState)
    builder.add_node('assistant', assistant_node)
    builder.add_node('tools', ToolNode(tools))
    builder.add_edge(START, 'assistant')
    builder.add_conditional_edges('assistant', tools_condition)
    builder.add_edge('tools', 'assistant')

    
    return builder.compile()

def create_task_agent(tools):
    return build_graph(tools)

def invoke(graph, user_input: str):
    messages = {'messages': [system_msg, HumanMessage(content=user_input)]}
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke(messages)
    return result['messages'][-1].content if result['messages'] else None