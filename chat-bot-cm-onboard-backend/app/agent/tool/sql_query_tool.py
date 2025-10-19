from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.tools import tool
from app.agent.llm_manager import get_llm
from sqlalchemy import text
from app.core.database import SessionLocal
import traceback


@tool
def sql_query_tool(user_query: str) -> str:

    """
    Generate and Execute SQL query from user_query using SQLAlchemy.
    """

    try:
        llm = get_llm(temperature=0)
        system_message = (
            "You are an expert SQL generator. "
            "Given a user's natural language request, output **only the SQL query** — nothing else. "
            "Do not include explanations, comments, or markdown. "
            "Use MySQL syntax.\n\n"
            "Database schema:\n"
            "suppliers(supplier_id, supplier_name, contact_person, phone_number, email, address)\n"
            "pharmacy_inventory(drug_id, drug_name, category, brand, unit_price, quantity_in_stock, expiry_date, supplier_id, reorder_level, location)\n"

        )

        messages = [
            SystemMessage(content=system_message),
            HumanMessage(content=user_query)
        ]

        response = llm.invoke(messages)
        sql_query = response.content.strip()

        print(f" LLM Generated Query:\n{sql_query}")

        if not any(sql_query.lower().startswith(k) for k in ["select", "insert", "update", "delete"]):
            return "The LLM did not generate a valid SQL query."

    except Exception as e:
        print(traceback.format_exc())
        return f"Error generating query: {e}"

    session = SessionLocal()
    try:
        result = session.execute(text(sql_query))

        if sql_query.lower().startswith("select"):

            rows = result.fetchall()
            keys = result.keys()
            data = [dict(zip(keys, row)) for row in rows]
            print(f" data:\n{data}")
            system_message2 = (
                "You are a warm, engaging, and professional assistant 🤝. "
                "Given SQL query results (in JSON), answer the user's question clearly. "
                "Be concise but friendly — use  emojis and bullet points for clarity. use things like points be informative\n\n"
                "- If no data found, say 'No data found 😕'.\n"
                "after answering engage with the user to prolong the conversation\n\n"
            )


            messages2 = [
                SystemMessage(content=system_message2),
                HumanMessage(content=f"User question: {user_query}\n\nSQL result: {data}")
            ]
            llm2 = get_llm(temperature=0.85)
            response2 = llm2.invoke(messages2)
            print(f" response2:\n{response2}")
            return response2.content
        else:
            session.commit()
            return "Query executed successfully."


    except Exception as e:
        session.rollback()
        print(traceback.format_exc())
        return f"Error executing query: {e}"

    finally:
        session.close()

