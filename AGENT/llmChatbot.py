#we are loading the environment variables from the .env file

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
model = init_chat_model("llama-3.3-70b-versatile", model_provider="groq")
response = model.invoke("How do you make paper out of trees. Explain to a 7 year old in easy way?")
print(response.content)
