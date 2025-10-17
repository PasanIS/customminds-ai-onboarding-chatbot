import asyncio

from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate

from app.ai.llm_manager import get_llm


def _generate_reply(self, message: str) -> str:

    llm = get_llm()

    def blocking_chain_run(msg: str):
        prompt = PromptTemplate(
            input_variables=["message"],
            template="You are a helpful assistant. Answer the following question: {message}"
        )

        chain = LLMChain(llm=llm, prompt=prompt)
        return chain.run(msg)

    return asyncio.to_thread(blocking_chain_run, message)