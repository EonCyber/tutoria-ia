from tasks.google_tasks import GoogleTasks
from datetime import datetime

def make_create_task_tool(google_tasks: GoogleTasks):
    """
    Cria uma ferramenta para criar tarefas no Google Tasks e enviar mensagens de confirmação via Telegram.
    """
    def create_google_task(title: str, due: str) -> str:
        """
          Cria uma tarefa no Google Tasks. Devolve uma mensagem de sucesso.
          - title: Título da tarefa a ser criada.
          - due: Data de vencimento da tarefa no formato ISO 8601 (ex: '2023-10-31T12:00:00Z').
        """
        result = google_tasks.create_task(title, due)
        message = f"✅ Tarefa criada com sucesso: {result.get('title')} para {due}"
        return message
    return create_google_task

def get_today_date() -> str:
    """
        Retorna a data atual no formato ISO 8601 (UTC), 
        ex: 2025-07-07T00:00:00Z, útil para saber o dia de hoje e qual data usar para criar tarefas.
    """
    return datetime.now().isoformat() + "Z"