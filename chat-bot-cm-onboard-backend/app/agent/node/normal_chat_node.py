from app.agent.agent_state import AgentState
from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.llm_manager import get_llm

def normal_chat_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.8)
    history = state.get("messages", [])
    user_query = state.get("user_query", "")

    llm_message = history + [HumanMessage(content=user_query)]
    print("normal_chat_node ",llm_message)
    system_message = (
        "You are a friendly pharmacy chatbot.\n"
        "Respond warmly to casual greetings, feelings, jokes, and small talk.\n"
        "Do NOT mention tools, routes, databases, or SQL.\n"
        "Use emojis, line breaks, and a friendly tone.\n"
    )


    #user_query = state.get("user_query", "")
    messages = [ SystemMessage(content=system_message),] + llm_message

    response = llm.invoke(messages)
    state["reply"] = response.content.strip()
    return state