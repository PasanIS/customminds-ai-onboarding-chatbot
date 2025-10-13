from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from app.ai.query_service import handle_sql_queries
from app.core.config import settings

# prompt template
prompt = PromptTemplate(
    input_variables=["message"],
    template="You are a helpful assistant. Answer the following question: {message}"
)

# Initialize the chat model
llm = ChatOpenAI(
    openai_api_key=settings.OPENAI_API_KEY,
    model_name="gpt-3.5-turbo"
)

# Function to generate a reply
# def generate_reply(message: str) -> str:
#     chain = LLMChain(llm=llm, prompt=prompt)
#     response = chain.run(message)
#     return response

# Function to generate a reply
async def generate_reply(message: str, session_id: str = None) -> str:

    # use normal LLM or SQL agent
    keyword = ["data", "records", "show", "list", "how many", "count", "sum", "average"]

    # check (DB related or not)
    if any(kw in message.lower() for kw in keyword):
        sql_response = await handle_sql_queries(message)
        if "reply" in sql_response:
            return sql_response["reply"]
        else:
            return f"Error: {sql_response['error']}"

    # default (normal LLM)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(message)