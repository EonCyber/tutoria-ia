import asyncio
from chat.tui import AiChatApp
from ai.human_loop import AssistantHumanLoop
from ai.human_as_tool import AssistantHumanHaatLoop
async def main():
    agent = await AssistantHumanHaatLoop(user_id="ian-123").async_init()
    app = AiChatApp(agent=agent)
    
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())
