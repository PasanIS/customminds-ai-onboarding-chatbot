from langchain_core.messages import SystemMessage, HumanMessage
from app.agent.agent_state import AgentState
from app.agent.llm_manager import get_llm

def chatbot_node(state: AgentState) -> AgentState:
    llm = get_llm(temperature=0.0)

    history = state.get("messages", [])
    user_query = state.get("user_query", "")
    llm_message = history + [HumanMessage(content=user_query)]

    print("chatbot_node ",llm_message)

    system_message = (
        "You are the routing layer of a private pharmacy chatbot system.\n"
        "You decide whether the query should be answered normally (as friendly small talk) "
        "or sent to the database tool.\n\n"
        "- Reply ONLY with database_query_tool or normal_chat.\n"
        "- Do NOT output Unknown tool decision.\n"
        "- Never show SQL, queries, tables, or databases as the output in UI.\n"

        "🚫 IMPORTANT:\n"
        "- NEVER route to web search. This chatbot does not use the internet.\n"
        "- Users are always referring to internal pharmacy/business data, unless clearly casual.\n"
        "- Handle spelling mistakes automatically.\n\n"

        "✅ Route to 'database_query_tool' when the user:\n"
        "- Asks about drugs, stock, expiry, inventory, suppliers, employees, purchases, sales, revenue.\n"
        "- Asks to list, show, count, calculate, filter, search, check availability.\n"
        "- Asks about totals, averages, low stock, cost, value, customers, doctors, prescriptions.\n"
        "- Mentions dates, comparison (today, yesterday, last week).\n"
        "- Asks for numbers from the system.\n"
        "- Is vague but smells like business context (e.g., 'What do we have low?', 'How many left?').\n\n"

        "💬 Handle as normal conversation when user:\n"
        "- Says hello, hi, good morning.\n"
        "- Asks how you are.\n"
        "- Gives compliments, feedback.\n"
        "- Asks for jokes, stories, motivation.\n"
        "- Talks about feelings.\n"
        "- Chitchat that is NOT about business data.\n\n"

        "📌 CLARIFICATION RULE:\n"
        "- IF YOU ARE UNSURE → choose database_query_tool anyway.\n"
        "- Only allow normal chat when it's 100% obvious.\n\n"

        "🧠 DO NOT output explanations, reasoning, or context.\n"
        "Reply with ONLY one of these (exactly):\n"
        "- database_query_tool\n"
        "- normal_chat\n"
    )


    user_query = state.get("user_query", "")
    messages = [ SystemMessage(content=system_message),] + llm_message

    response = llm.invoke(messages)

    state["reply"] = response.content.strip()
    return state
