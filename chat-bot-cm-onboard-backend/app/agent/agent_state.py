from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages


class AgentState(TypedDict):

    messages: Annotated[List, add_messages]
    user_query: str
    decision: str
    reply: str