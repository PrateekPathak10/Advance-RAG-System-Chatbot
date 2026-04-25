from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

groq_api_key= os.getenv("groq_api_key")

def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key
        )
