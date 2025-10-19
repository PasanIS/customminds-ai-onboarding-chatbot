from langgraph.constants import END
from langgraph.graph import StateGraph
from app.agent.agent_state import AgentState
from app.agent.node.chatbot_node import chatbot_node
from app.agent.node.tool_caller_node import tool_caller_node


def create_graph():
    graphflow = StateGraph(AgentState)

    def route_after_chatbot(state: AgentState) -> str:
        decision = state.get("reply", "").strip().lower()
        if decision in ["database_query_tool", "web_search_tool"]:
          #state["decision"] = decision
            return "call_tools"
        else:
            return "answer"


    graphflow.add_node("chatbot_node", chatbot_node)
    graphflow.add_node("tool_caller_node", tool_caller_node)

    graphflow.set_entry_point("chatbot_node")
    graphflow.add_conditional_edges(
        "chatbot_node",
        route_after_chatbot,
        {
            "call_tools": "tool_caller_node",
            "answer": END
        }
    )
    graphflow.add_edge("tool_caller_node", END)

    return graphflow.compile()
