from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.agent_state import AgentState
from app.agent.llm_manager import get_llm

def chatbot_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.0)

    system_message = (
        "You are a routing assistant for a chatbot system.\n"
        "Decide which tool should handle the user's query.\n"
        "If it is a too call you must reply ONLY with one of the following (nothing else): No explanations. No reasoning. Reply only with the tool name exactly.\n"
        "- 'database_query_tool' → if the question involves database information, counting, listing, or retrieving records.\n"
        "- 'web_search_tool' → if the question requires searching the internet.\n"
        "If it is not a tool call have a warm conversation with user"
    )

    user_query = state.get("user_query", "")
    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=user_query)
    ]

    response = llm.invoke(messages)

    state["reply"] = response.content.strip()
    return state
