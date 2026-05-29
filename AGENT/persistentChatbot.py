import os
from dotenv import load_dotenv
load_dotenv()
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver


import streamlit as st
st.title("Rajat's Chatbot App")


MEMORY_DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".db")
MEMORY_DB_PATH = os.path.join(MEMORY_DB_DIR, "agent_memory.db")


os.makedirs(MEMORY_DB_DIR, exist_ok=True)


if "messages" not in st.session_state:
  st.session_state.messages = []


with SqliteSaver.from_conn_string(MEMORY_DB_PATH) as checkpointer:
   agent = create_agent(
       model="openai:gpt-4o",
       tools=[],
       checkpointer=checkpointer,
   )


   def stream_graph_updates(user_input : str):
       assistant_response = ""
       with st.chat_message("assistant"):
           message_placeholder = st.empty()
           for event in agent.stream({"messages": [{"role": "user", "content": user_input}]}, {"configurable": {"thread_id": "def"}}):
               for value in event.values():
                   new_text = value["messages"][-1].content
                   assistant_response += new_text
                   message_placeholder.markdown(assistant_response)


       st.session_state.messages.append(("assistant", assistant_response))


   # Display previous chat history
   for role, message in st.session_state.messages:
       with st.chat_message(role):
           st.markdown(message)


   prompt = st.chat_input("What is your question?")
   if prompt:
   # Display user input as a chat message
       with st.chat_message("user"):
           st.markdown(prompt)
       # Append user input to session state
       st.session_state.messages.append(("user", prompt))
  
       # Get response from the chatbot based on user input
       response = stream_graph_updates(prompt)
