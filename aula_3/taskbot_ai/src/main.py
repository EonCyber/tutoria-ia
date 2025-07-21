from bot.poll import start_telegram_polling
from tasks.google_tasks import GoogleTasks
from tasks.credentials import GoogleCredentialProvider
from tools.tools import make_create_task_tool, get_today_date
from agent.task_agent import create_task_agent, invoke


creds = GoogleCredentialProvider().fetch_credential()
google_tasks = GoogleTasks(creds)
create_task_tool = make_create_task_tool(google_tasks)
## Edit task
## List Tasks
## Complete Task
tools = [create_task_tool, get_today_date]
agent = create_task_agent(
    tools=tools,
)

if __name__ == "__main__":
    start_telegram_polling(agent, invoke)