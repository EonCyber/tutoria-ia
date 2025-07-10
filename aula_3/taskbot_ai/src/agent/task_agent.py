from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from agent.prompt import SYSTEM_PROMPT
from langgraph.graph import MessagesState
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

class TaskAgent:

    def __init__(self, tools):
        self.memory = MemorySaver()
        self.system_msg = SystemMessage(    
            content=SYSTEM_PROMPT,
        )
        self.tools = tools
        print('Inicializando OpenAi LLM com Ferramentas...')
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
        ).bind_tools(tools)
        print('Construindo grafos...')
        self.graph = self.build_graph()
        print('Agente de Tarefas Construído com Sucesso!')
    
    def build_graph(self):
        builder = StateGraph(MessagesState)

        # Definindo um Nodo Assistente
        def assistant(state: MessagesState):
            messages = state['messages']
            response = self.llm.invoke(messages)
            return {"messages": messages + [response]}
        
        builder.add_node('assistant', assistant)
        builder.add_node('tools', ToolNode(self.tools))
        builder.add_edge(START, 'assistant')
        builder.add_conditional_edges('assistant', tools_condition)
        builder.add_edge('tools', 'assistant')

        builder.compile().to_json_file("langgraph.json")
        return builder.compile(checkpointer=MemorySaver())

    def invoke(self, user_input: str):
        """
        Invokes the task agent with the user input.
        """
        # Create a new state with the user input
        messages = { 'messages': [
            self.system_msg,
            HumanMessage(content=user_input)
        ]}
        config = {"configurable": {"thread_id": "1"}}
        # Run the graph
        result = self.graph.invoke(messages, config)
        
        # Return the response from the assistant
        return result['messages'][-1].content if result['messages'] else None