from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.agent_state import AgentState
from app.ai.llm_manager import get_llm


def greeting_node(state: AgentState) -> AgentState:
    llm = get_llm()

    print("Greeting node invoked with state:", state)
    system_message = (
        "You are a friendly and helpful AI assistant. "
        "Greet the user warmly and offer your assistance. "
        "Keep the greeting concise and engaging."
    )

    message = [
        SystemMessage(content=system_message),
        HumanMessage(content=state["user_query"])
    ]

    response = llm.invoke(message)
    print("res:", response)
    state["reply"] = response.content
    return state