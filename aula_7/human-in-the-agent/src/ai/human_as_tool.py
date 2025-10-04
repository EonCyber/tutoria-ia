from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver
from operator import add
from typing import Annotated
from langchain_mcp_adapters.client import MultiServerMCPClient
from ai.tools.config import MCP_SERVERS_CONFIG
from ai.prompts.rules import SYSTEM_RULES, CONTRACT_GENERATION_PROMPT, INFORMATION_NEEDED_PROMPT, REVIEW_CONTRACT_PROMPT, EDITOR_RULES
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import datetime
import re
import os
from dotenv import load_dotenv
load_dotenv()


class ToolsLoader:    
    async def get_tools(self, mcp_config: dict):
        return await MultiServerMCPClient(mcp_config).get_tools()
    
def replace_reducer(old, new):
    return new
# STATE --> ESTADO DO GRAFO 
class AssistantState(MessagesState):
    human_feedback: Annotated[bool, replace_reducer] = False
    contract: Annotated[list[str], add]

def _sanitize_filename(name: str) -> str:
    # Remove caracteres que dão problema em filenames e deixa só letras, números, -, _
    name = name.strip()
    # substitui espaços por _
    name = re.sub(r"\s+", "_", name)
    # remove chars indesejados
    name = re.sub(r"[^A-Za-z0-9_\-\.]", "", name)
    return name or "contract"

def _timestamp_str() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

CONTRACTS_DIR = "./contracts"

class AssistantHumanHaatLoop:

    def __init__(self, user_id: str):
        self.thread = { "configurable":  { "thread_id": user_id }}
        self.graph = None
        self.llm = None
        self.tools = None  
        self.contract_tool = None 
        self.human_review = False

    async def async_init(self):
        self.tools = await ToolsLoader().get_tools(MCP_SERVERS_CONFIG)
        self.assistant_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7).bind_tools(self.tools)
        self.graph = await self.build_graph()
        return self
    
    def make_assistant_node(self, system_prompt):
        def assistant_node(state: AssistantState):
            final_prompt = ChatPromptTemplate.from_messages([SystemMessage(content=system_prompt),
                                                             MessagesPlaceholder(variable_name='history')]
                                                             ).format_messages(
                                                                 history=state["messages"]
                                                             )
            return { "messages": [self.assistant_llm.invoke(final_prompt)] }
        return assistant_node
    def make_editor_node(self, system_prompt):
        def editor_node(state: AssistantState):
            print("Invocando Editor Node")
            final_prompt = ChatPromptTemplate.from_messages([("system", system_prompt),
                                                             MessagesPlaceholder(variable_name='history')]
                                                             ).format_messages(
                                                                 history=state["messages"],
                                                                 contract=state["contract"][-1]
                                                             )
            return { "messages": [self.assistant_llm.invoke(final_prompt)], "human_feedback": True }
        return editor_node
    
    # TODO SPECIAL NODE 
    def make_human_approval_node(self):
        def human_approval_node(state: AssistantState):
            pass
        return human_approval_node
  
    def make_conditional_node(self):
        def conditional_node(state: AssistantState) -> str:
            print("Invocando Conditional Node")
            messages = state["messages"]

            # 1. Se a última mensagem da LLM chamou tool → vai para tools
            ai_message = messages[-1] if messages else None
            if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
                print("[LOG] Nodo 'save_contract_condition' detectou tool_calls na última mensagem:")
                for call in ai_message.tool_calls:
                    print("   - tool:", call.get("name"))
                    print("   - args:", call.get("args"))
                print(f"DECISAO: need_tools" )
                return "need_tool"
            # 2. 
            final_prompt = ChatPromptTemplate.from_messages([SystemMessage(content= INFORMATION_NEEDED_PROMPT),
                                                             MessagesPlaceholder(variable_name='history')]
                                                             ).format_messages(
                                                                 history=messages
                                                             )
            
            answer = self.assistant_llm.invoke(final_prompt).content
            print(f"DECISAO: {answer}" )
            if answer == "CONTRACT":
                return "has_contract_info"
            return "end"
        return conditional_node

    def make_generate_contract_node(self):
        """ Deve usar historico das mensagens para mandar para a llm 
            junto de um prompt indicado gerar um contrato em markdown
        """
        def generate_contract_node(state: AssistantState):
            messages = state.get('messages')
            final_prompt = ChatPromptTemplate.from_messages([SystemMessage(content= CONTRACT_GENERATION_PROMPT),
                                                             MessagesPlaceholder(variable_name='history')]
                                                             ).format_messages(
                                                                 history=messages
                                                             )
            # TODO
            print("Invocando nodo de Geracao de Contrato")
            contract_generated = self.assistant_llm.invoke(final_prompt).content

            # Perguntar pro usuário se o contrato precisa de revisao 
            final_prompt_ask = ChatPromptTemplate.from_messages([("system", REVIEW_CONTRACT_PROMPT)]
                                                             ).format_messages(
                                                                 contract=contract_generated
                                                             )
            final_message = self.assistant_llm.invoke(final_prompt_ask).content

            return { "messages": [final_message], "contract": [contract_generated], "human_feedback": True }
        return generate_contract_node
    
    def make_save_contract_condition(self):
        """ Deve usar historico das mensagens para mandar para a llm 
            junto de um prompt indicado DECIDIR se vai gerar contrato em markdown
        """
        def save_contract_condition(state: AssistantState):
            print("Invocando save_contract_condition")
            messages = state['messages'][-3:]
            constract = state['contract'][-1]
            final_prompt = ChatPromptTemplate.from_messages([
                                                            MessagesPlaceholder(variable_name="history"),
                                                            ("system",""" 
                                                                Você é um classificador de estado da conversa sobre contratos.

                                                                Sua tarefa é analisar as últimas mensagens em qual situação ela se enquadra.
                                        
                                                                Categorias possíveis:
                                                                - approved: contrato está finalizado e pronto para ser salvo.
                                                                - need_info: ainda faltam informações, você deve pedir esclarecimentos ao usuário antes de prosseguir.
                                                                - edit_ready: já existe informação suficiente para editar o contrato diretamente.

                                                                Regras:
                                                                - Não adicione explicações, texto extra ou formatação.
                                                                - Responda exclusivamente com uma das palavras: approved, need_info ou edit_ready.\n
                                                            """), 
                                                            ]
                                                             ).format_messages(
                                                                 history=messages,
                                                             )
            
            answer = self.assistant_llm.invoke([constract] + final_prompt).content.strip()
            print(answer)
            return answer
        return save_contract_condition
    
    
    def make_save_contract_node(self):
        def save_contract_node(state: AssistantState):
            content = state["contract"][-1]
            filename = "contrato_troca_pokemon" 
            # TODO
            print("Invocando Nodo de Salvamento de Contrato")
            try:
                base = filename
                base_clean = _sanitize_filename(base)
                fname = f"{base_clean}_{_timestamp_str()}.md"
                path = os.path.join(CONTRACTS_DIR, fname)

               
                with open(path, "w", encoding="utf-8") as f:
                    f.write(content)

                return {"messages": [AIMessage(content=f"Contrato Salvo! Local: {path}")], "human_feedback": False}
            except Exception as e:
                return {"messages": [AIMessage(content=f"Não consegui salvar contrato. Erro: {e}")], "human_feedback": False}

        return save_contract_node
    def save_graph_img(self, graph):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"src/ai/img/graph_{timestamp}.mmd"

        mermaid_code = graph.get_graph(xray=True).draw_mermaid()
        with open(file_path, "w") as f:
            f.write(mermaid_code)

    async def build_graph(self):
        tool_node = ToolNode(self.tools)
        save_contract_node = self.make_save_contract_node()
        assistant_node = self.make_assistant_node(SYSTEM_RULES)
        editor_node = self.make_editor_node(EDITOR_RULES)
        
        conditional_node = self.make_conditional_node()
        save_contract_condition = self.make_save_contract_condition()

        generate_contract_node = self.make_generate_contract_node()
        human_approval_node = self.make_human_approval_node()
        builder = StateGraph(AssistantState)
        # Nodes Definition
        builder.add_node('assistant', assistant_node)
        builder.add_node('contract_editor', editor_node)
        builder.add_node('human_approval_node', human_approval_node)
        builder.add_node('generate_contract_node', generate_contract_node)
        builder.add_node('tools', tool_node)
        builder.add_node('save_contract_node', save_contract_node)
        # Edges
        builder.add_edge(START,'assistant')
        builder.add_conditional_edges('assistant', conditional_node, { 
                                                    "need_tool": "tools",
                                                    "has_contract_info": "generate_contract_node", 
                                                    "end": END }
                                                    )
        builder.add_edge('tools', 'assistant')
        builder.add_edge('generate_contract_node', 'human_approval_node')
        builder.add_edge('human_approval_node', 'contract_editor')
        builder.add_conditional_edges('contract_editor', save_contract_condition, { 
            "approved": 'save_contract_node', 
            "edit_ready": 'generate_contract_node', 
            "need_info": "human_approval_node"}
            )
        builder.add_edge('save_contract_node', END)

        # Memory
        memory = InMemorySaver()
        graph = builder.compile( interrupt_before=["human_approval_node"], checkpointer=memory)
        
        self.save_graph_img(graph)

        return graph
    
    def extract_ai_answer(self, final_state):
        return final_state['messages'][-1].content
    
    async def ask(self, input_msg:str):
        message_state = {"messages": [HumanMessage(content=input_msg)]}
        answer = ""
        last_state = None

        if (self.human_review == False):
            async for state_full  in self.graph.astream(message_state, config=self.thread, stream_mode="values"):
                last_state = state_full

            state_vals = last_state.get("channel_values") or last_state.get("values") or last_state
            messages = state_vals.get("messages", [])
            answer = messages[-1].content
            self.human_review = state_vals["human_feedback"]

        elif (self.human_review): 
            # Atualiza o state usando o nodo human_approval_node
            self.graph.update_state(self.thread, { "messages": [HumanMessage(content=input_msg)], "human_feedback": False }, as_node="human_approval_node") 
            # Destrava o grafo
            for state_full in self.graph.stream(None, self.thread, stream_mode="values"):
                last_state = state_full

            state_vals = last_state.get("channel_values") or last_state.get("values") or last_state
            messages = state_vals.get("messages", [])
            answer = messages[-1].content
            self.human_review = state_vals["human_feedback"]

        return answer

        