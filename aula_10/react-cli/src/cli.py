from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
import itertools
import threading
import time
import traceback
from langchain_core.messages import AIMessage
from langfuse.langchain import CallbackHandler
from langfuse import get_client
import uuid

from dotenv import load_dotenv
load_dotenv()

langfuse = get_client()
session_seed = str(uuid.uuid4())
session_id = langfuse.create_trace_id(seed=session_seed)
langfuse_handler = CallbackHandler()

class ChatBotApp:

    def __init__(self, agent):
        self.agent = agent 
        self.console = Console()
        self.spinner = itertools.cycle(["|", "/", "-", "\\"])

    def run(self):
        console = self.console
        console.print("[bold green]Bem-vindo ao Chat CLi[/bold green]")
        console.print("[cyan]Digite 'sair' ou 'exit' ou 'quit' para encerrar[/cyan]")

        while True:
            user_input = console.input("[bold yellow]Você:[/bold yellow]")
            if user_input.lower() in ["sair", "exit", "quit"]:
                console.print("[red]Encerrando chat...[/red]")
                break
            # Painel de Eco do User Input
            console.print(Panel(Text(user_input, style="bold yellow"), title="Você"))

            response = None
            def generate_response():
                nonlocal response
                try:
                    # response = self.agent.invoke({ "messages": user_input }, config={ "callbacks": [langfuse_handler] })
                    response = self.agent.invoke({ 
                        "messages": user_input }, 
                        config={ "callbacks": [langfuse_handler], 
                                "metadata": { "langfuse_session_id": session_id }
                            }
                        )
                except Exception as e:
                    print(traceback.format_exc())
                    response = AIMessage(content=f"Erro: {e}")
            thread = threading.Thread(target=generate_response)
            thread.start()

            with Live("", console=console, refresh_per_second=10) as live:
                while thread.is_alive():
                    live.update(f"[bold cyan] IA está pensando {next(self.spinner)}")
                    time.sleep(0.1)
                live.update("")

            console.print(Panel(Text(response["messages"][-1].content, style="bold cyan"),title="IA"))