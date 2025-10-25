from langchain_core.messages import HumanMessage, AIMessage
from app.agent.agent_state import AgentState
from app.agent.tool.sql_query_tool import sql_query_tool
import traceback

def tool_caller_node(state: AgentState) -> AgentState:
    try:
        decision = state.get("reply", "").strip().lower()
        messages = state.get("messages", [])
        query = messages[-1].content

        message_history = []
        for msg in messages[:-1]:
            if isinstance(msg, HumanMessage):
                message_history.append({"role": "user", "content": msg.content})
            elif isinstance(msg, AIMessage):
                message_history.append({"role": "assistant", "content": msg.content})

        if decision == "database_query_tool":
            tool_input = message_history + [{"role": "user", "content": query}]

            result = sql_query_tool.invoke({"user_query": tool_input})
            state["reply"] = result

        elif decision == "web_search_tool":
            state["reply"] = "Web search tool not implemented yet."

        else:
            pass

    except Exception as e:
        print(traceback.format_exc())

    return state
