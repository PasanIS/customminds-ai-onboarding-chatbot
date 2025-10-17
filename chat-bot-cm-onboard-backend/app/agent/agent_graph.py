from langgraph.constants import END
from langgraph.graph import StateGraph
from app.agent.agent_state import AgentState
from app.agent.node.greeting_node import greeting_node


def create_graph():
    graphflow = StateGraph(AgentState)

    graphflow.add_node("greeting_node", greeting_node)
    graphflow.set_entry_point("greeting_node")
    graphflow.add_edge("greeting_node", END)
    return graphflow.compile()
