# llm setup---OpenAI

from langchain_openai import ChatOpenAI
from app.core.config import settings

def get_llm():

    # init and return Open AI llm client
    return ChatOpenAI(
        openai_api_key=settings.OPENAI_API_KEY,
        model_name="gpt-5-nano",
        temperature=0
    )