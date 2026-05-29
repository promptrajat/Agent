#https://docs.langchain.com/oss/python/langchain/short-term-memory
import os
from dotenv import load_dotenv
load_dotenv()


from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver 


agent = create_agent(
 model="groq:llama-3.3-70b-versatile",
 tools=[],
 checkpointer=InMemorySaver()
)
response = agent.invoke(
 {"messages": [{"role": "user", "content": "who is dhoni"}]},
 {"configurable": {"thread_id": "1"}},
)
print(response["messages"][-1].content)


response = agent.invoke(
 {"messages": [{"role": "user", "content": "when was he born?"}]},
 {"configurable": {"thread_id": "1"}},
)
print(response["messages"][-1].content)