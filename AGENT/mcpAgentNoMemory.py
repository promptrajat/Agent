import os
from dotenv import load_dotenv
load_dotenv()


from langchain.agents import create_agent


agent = create_agent(
 model="groq:llama-3.3-70b-versatile",
 tools=[]
)
response = agent.invoke(
 {"messages": [{"role": "user", "content": "who is dhoni"}]}
)
print(response["messages"][-1].content)


response = agent.invoke(
 {"messages": [{"role": "user", "content": "when was he born?"}]}
)
print(response["messages"][-1].content)