import asyncio
import websockets

connections = {}

async def handler(websocket, path):
    client_id = f"agente-{len(connections)+1}"
    connections[client_id] = websocket
    print(f"🔌 Nova conexão recebida: {client_id}")

    try:
        async for question in websocket:
            print(f"🤖 Pergunta recebida de {client_id}: {question}")

            # pede input humano
            answer = input("👤 Sua resposta: ")

            # devolve a resposta para o agente
            await websocket.send(answer)
            print(f"✅ Resposta enviada para {client_id}")
    except websockets.exceptions.ConnectionClosed:
        print(f"❌ Conexão encerrada: {client_id}")
    finally:
        connections.pop(client_id, None)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Servidor humano rodando em ws://localhost:8765")
        await asyncio.Future()  # roda para sempre

if __name__ == "__main__":
    asyncio.run(main())
