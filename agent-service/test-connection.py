import os
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

llm = ChatNVIDIA (
    model="nvidia/nemotron-3.5-lightning-30b-a3b",
    api_key=os.getenv("NVIDIA_API_KEY")
)

response = llm.invoke("Say hello in one sentence.")
print(response.content)