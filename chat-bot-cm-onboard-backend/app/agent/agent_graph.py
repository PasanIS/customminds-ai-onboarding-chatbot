from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import END
from langgraph.graph import StateGraph
from app.agent.agent_state import AgentState
from app.agent.node.chatbot_node import chatbot_node
from app.agent.node.normal_chat_node import normal_chat_node
from app.agent.node.tool_caller_node import tool_caller_node


def create_graph():
    graphflow = StateGraph(AgentState)

    def route_after_chatbot(state: AgentState) -> str:
        decision = state.get("reply", "").strip().lower()
        if decision == "database_query_tool":
            return "call_tools"
        elif decision == "normal_chat":
            return "casual"
        else:
            return "call_tools"


    graphflow.add_node("chatbot_node", chatbot_node)
    graphflow.add_node("tool_caller_node", tool_caller_node)
    graphflow.add_node("normal_chat_node", normal_chat_node)

    graphflow.set_entry_point("chatbot_node")

    graphflow.add_conditional_edges(
        "chatbot_node",
        route_after_chatbot,
        {
            "call_tools": "tool_caller_node",
            "casual": "normal_chat_node"
        }
    )

    graphflow.add_edge("tool_caller_node", END)
    graphflow.add_edge("normal_chat_node", END)

    memory = MemorySaver()
    graph = graphflow.compile(checkpointer=memory)
    return graph
