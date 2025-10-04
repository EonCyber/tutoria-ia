from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
import threading
import time
import itertools
import asyncio

class AiChatApp:
    def __init__(self, agent):
        self.agent = agent
        self.console = Console()
        self.spinner = itertools.cycle(["|", "/", "-", "\\"])
    def run(self):
        console = self.console
        console.print("[bold green]Bem-vindo ao Chat CLI![/bold green]")
        console.print("[cyan]Digite 'sair' para encerrar[/cyan]\n")

        while True:
            user_input = console.input("[bold yellow]Você:[/bold yellow] ")
            if user_input.lower() in ["sair", "exit", "quit"]:
                console.print("[red]Encerrando chat...[/red]")
                break

            console.print(Panel(Text(user_input, style="bold yellow"), title="Você"))

            resposta = None

            def generate_response():
                nonlocal resposta
                try:
                    resposta = asyncio.run(self.agent.ask(user_input))
                except Exception as e:
                    resposta = f"[red]Erro: {e}[/red]"

            thread = threading.Thread(target=generate_response)
            thread.start()

            # Live para atualizar a mesma linha com cores
            with Live("", console=console, refresh_per_second=10) as live:
                while thread.is_alive():
                    live.update(f"[bold cyan]IA está pensando {next(self.spinner)}")
                    time.sleep(0.1)
                # Quando terminar, limpa o spinner
                live.update("")
    
            console.print(Panel(Text(resposta, style="bold cyan"), title="IA"))
     