from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.checkpoint.memory import MemorySaver
import asyncio
from dotenv import load_dotenv
import os

# os.environ["GROQ_API_KY"] -- give the key
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


async def run_agent():
    print("Step 1: Creating client...")
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-github"
                ],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
                },
                "transport": "stdio"
            },
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "C:\\Users\\RajatBhatia\\Documents\\Learning\\AI\\AGENT"
                ],
                "transport": "stdio"
            }
        }
    )

    print("Step 2: Client created, getting tools...")
    try:
        tools = await client.get_tools()
        print("Step 3: Tools loaded:", [t.name for t in tools])
    except Exception as e:
        print(f"FAILED at get_tools: {type(e).__name__}: {e}")
        return

    memory = MemorySaver()
    agent = create_agent("groq:llama-3.3-70b-versatile", tools, checkpointer=memory)
    config = {"configurable": {"thread_id": "1"}}

    # --- Turn 1: Create a file ---
    print("\nTurn 1: Creating file...")
    try:
        response = await agent.ainvoke(
            {"messages": "Use the write_file tool to create a file named rajat.txt in C:\\Users\\RajatBhatia\\Documents\\Learning\\AI\\AGENT with content 'Hello from Rajat!'"},
            config
        )
        print(response["messages"][-1].content)
    except Exception as e:
        print(f"Turn 1 FAILED: {type(e).__name__}: {e}")

    # --- Turn 2: List directory ---
    print("\nTurn 2: Listing directory...")
    try:
        response = await agent.ainvoke(
            {"messages": "Use the list_directory tool to list all files in C:\\Users\\RajatBhatia\\Documents\\Learning\\AI\\AGENT"},
            config
        )
        print(response["messages"][-1].content)
    except Exception as e:
        print(f"Turn 2 FAILED: {type(e).__name__}: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(run_agent())
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")