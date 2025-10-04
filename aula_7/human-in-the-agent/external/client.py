import asyncio
import websockets

async def test():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        await ws.send("ping")
        resp = await ws.recv()
        print("Resposta:", resp)

asyncio.run(test())