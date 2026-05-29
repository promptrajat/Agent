import os
from dotenv import load_dotenv
load_dotenv()
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver  # 👈 needed for memory

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

async def run_agent():
    client = MultiServerMCPClient(
        {
            "github": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-github"],
                "env": {
                    "GITHUB_PERSONAL_ACCESS_TOKEN": GITHUB_TOKEN
                },
                "transport": "stdio"
            }
        }
    )
    tools = await client.get_tools()

    # 👇 MemorySaver lets the agent remember across multiple ainvoke calls
    memory = MemorySaver()
    agent = create_agent("groq:llama-3.3-70b-versatile", tools, checkpointer=memory)

    # same thread_id = same conversation memory
    config = {"configurable": {"thread_id": "1"}}

    # --- Turn 1: List root directory ---
    print("🔍 Turn 1: Listing root directory...")
    response = await agent.ainvoke(
        {"messages": "List the contents of the root directory of the GitHub repo. owner='promptrajat', repo='Agent', path=''"},
        config  # 👈 pass config here, not inside messages dict
    )
    print(response["messages"][-1].content)

    # --- Turn 2: Agent remembers Turn 1, goes deeper ---
    print("\n🔍 Turn 2: Listing subfolder contents...")
    response = await agent.ainvoke(
        {"messages": "Now list the contents of the folder you found in the previous step."},
        config  # 👈 same thread_id = agent remembers previous response
    )
    print(response["messages"][-1].content)

    # --- Turn 3: Summarize ---
    print("\n🤖 Turn 3: Summarizing...")
    response = await agent.ainvoke(
        {"messages": "Now summarize what this repository does based on the files you've seen."},
        config
    )
    print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(run_agent())