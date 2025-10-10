from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
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
def generate_reply(message: str) -> str:
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run(message)
    return response