import asyncio

async def run_agent():
    print("Inside run_agent!")
    
    from langchain_mcp_adapters.client import MultiServerMCPClient
    import os
    
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    
    print("Creating client...")
    client = MultiServerMCPClient(
        {
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
    print("Client created!")
    
    try:
        tools = await client.get_tools()
        print("Tools:", [t.name for t in tools])
    except Exception as e:
        print(f"get_tools FAILED: {type(e).__name__}: {e}")

if __name__ == "__main__":
    print("Starting...")
    try:
        asyncio.run(run_agent())
    except Exception as e:
        print(f"asyncio.run FAILED: {type(e).__name__}: {e}")
    print("Finished!")