from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from agent.task_agent import TaskAgent
import os
from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")

def build_message_handler(agent: TaskAgent):
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        chat_id = update.message.chat_id
        print(f"📨 Mensagem recebida: {text}")
        result = agent.invoke(text)
        print(f"🤖 Resposta do agente: {result}")
        await context.bot.send_message(chat_id=chat_id, text=result)
    return MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

def start_telegram_polling(agent: TaskAgent):
    app = ApplicationBuilder().token(TELEGRAM_API_KEY).build()
    handle_message = build_message_handler(agent)
    # Adiciona handler para qualquer mensagem de texto
    app.add_handler(build_message_handler(agent))

    print("🤖 Bot do Telegram rodando... esperando mensagens.")
    app.run_polling()