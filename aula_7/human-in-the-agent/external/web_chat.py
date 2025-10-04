from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uuid
import uvicorn

app = FastAPI(title="MCP Simulando um Web Chat")

class Question(BaseModel):
    message: str

class Answer(BaseModel):
    message_id: str
    reply: str

# Dicionário de mensagens pendentes
pending_responses: dict[str, asyncio.Future] = {}

@app.post("/ask")
async def ask_human(q: Question):
    message_id = str(uuid.uuid4())
    print(f"🌐 Pergunta enviada (id={message_id}): {q.message}")

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    pending_responses[message_id] = future

    try:
        # Espera a resposta do humano via webhook
        reply = await asyncio.wait_for(future, timeout=120.0)
        print(f"📩 Resposta recebida (id={message_id}): {reply}")
        return {"message_id": message_id, "reply": reply}  # retorna exatamente a mensagem recebida
    except asyncio.TimeoutError:
        print(f"⏱️ Timeout aguardando resposta para message_id={message_id}")
        raise HTTPException(status_code=408, detail="Timeout aguardando resposta")
    finally:
        pending_responses.pop(message_id, None)

@app.post("/webhook")
async def webhook_answer(a: Answer):
    future = pending_responses.get(a.message_id)
    if future is None:
        raise HTTPException(status_code=404, detail="Message ID não encontrado ou já respondido")
    
    if not future.done():
        future.set_result(a.reply)  # aqui resolvemos a Future com a mensagem recebida
        print(f"✅ Webhook recebeu resposta para message_id={a.message_id}: {a.reply}")

    return {"message_id": a.message_id, "reply": a.reply, "status": "ok"}  # retorna a mesma mensagem que chegou


def start_app(host: str = "127.0.0.1", port: int = 8000):
    """
    Inicia o FastAPI programaticamente usando uvicorn.
    """
    print(f"🚀 Iniciando app em http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_app()
