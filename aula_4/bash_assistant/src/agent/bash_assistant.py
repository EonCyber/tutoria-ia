from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from agent.prompt import SYSTEM_PROMPT
from langgraph.graph import MessagesState
from langchain_openai import ChatOpenAI
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, create_react_agent, tools_condition
from dotenv import load_dotenv

load_dotenv()

agent_memory = MemorySaver()
system_msg = SystemMessage(content=SYSTEM_PROMPT)


def make_agent_node(tools):
    return create_react_agent(
        model=ChatOpenAI(model="gpt-4o-mini", temperature=0.8).bind_tools(tools),
        tools=tools,
        prompt=SYSTEM_PROMPT
    )

def build_graph(tools):
    agent = make_agent_node(tools)
    builder = StateGraph(MessagesState)
    builder.add_node('agent', agent)
    builder.add_node('tools', ToolNode(tools))
    builder.add_edge(START, "agent")
    builder.add_conditional_edges('agent', tools_condition)

    return builder.compile()

def create_agent(tools):
    """
    Função para criar um agente com ferramentas específicas.
    Retorna o agente configurado.
    """
    return build_graph(tools)

def invoke(graph, user_input: str):
    messages = {'messages': [HumanMessage(content=user_input)]}
    config = {"configurable": {"thread_id": "1"}}
    result = graph.invoke(messages)
    return result['messages'][-1].content if result['messages'] else None