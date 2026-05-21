import os
from dotenv import load_dotenv
load_dotenv()


from langchain.agents import create_agent


def addFile(filename: str) -> None:
  """Create a new file in current directory"""
  if not os.path.exists(filename):
     with open(filename, "w") as f:
         pass
     print(f"File '{filename}' created.")
  else:
     print(f"File '{filename}' already exists.")


def addFolder(directory_name: str) -> None:
 """Create a new Directory in current directory"""
 if not os.path.exists(directory_name):
     os.mkdir(directory_name)
     print(f"Directory '{directory_name}' created.")
 else:
     print(f"Directory '{directory_name}' already exists.")


agent = create_agent(
  model="groq:llama-3.3-70b-versatile",
  tools=[addFile, addFolder]
)
# Run the agents
response = agent.invoke(
  {"messages": [{"role": "user", "content": "create a new directory with name TestAICharmDirectory"}]}
)
print(response["messages"][-1].content)