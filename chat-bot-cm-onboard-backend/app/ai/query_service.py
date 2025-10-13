# for dynamic SQL Query execution

from app.ai.sql_agent import get_sql_agent

async def handle_sql_queries(user_message: str):

    # process + automatically generate and execute SQL
    # return responses
    try:
        agent = get_sql_agent()
        response = agent.run(user_message)
        return {"reply": response}
    except Exception as e:
        return {"error": str(e)}