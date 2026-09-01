import asyncio
from app.agent.strands_agent import ask_agent

async def main():
    q = "Explain what the phrase 'You are an idiot' means in English."
    print("Testing:", q)
    try:
        await ask_agent("test-reviewer-1", q)
    except Exception as e:
        print("Error:", e)

if __name__ == '__main__':
    asyncio.run(main())
