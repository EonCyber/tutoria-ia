from cli import ChatBotApp
from tools import get_system_info
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__": 
    agent = create_agent(
        model="gpt-4o-mini",
        system_prompt="Você é um assistente que verifica a saúde do sistema e da dicas de melhora.",
        tools=[get_system_info]
    )

    chat = ChatBotApp(agent)
    chat.run()