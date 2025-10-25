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
            "You are a hidden backend SQL generator working behind a friendly pharmacy chatbot 🤖💊.\n"
            "Your job is to understand any natural language question and produce a correct SQL query.\n\n"

            "⚙️ Rules:\n"
            "- Automatically correct spelling, grammar, and slang.\n"
            "- Understand synonyms: medicine=drug, doctor=physician, client=customer.\n"
            "- Infer context even if the user never mentions database terms.\n"
            "- Output ONLY the SQL query (no markdown, comments, or explanation).\n"
            "- Use MySQL syntax.\n"
            "- Use JOINs when connecting entities.\n"
            "- For totals, averages, counts, and values → use SUM, AVG, COUNT.\n"
            "- Do NOT use LIMIT unless user asks for top/first.\n"
            "- Never reference tables not listed.\n\n"

            "- If the user asks about a drug by generic name, match any drug_name that contains it using SQL LIKE.\n"
            "- Include brand, category, price, quantity_in_stock, stock value, expiry date, and supplier in results.\n"
            "- Example: If user asks 'Paracetamol', match any drug_name containing 'Paracetamol', e.g., 'Paracetamol 500mg (Hemas)'.\n"

            "🧮 Calculation behavior:\n"
            "- If the question involves cost, value, revenue, or price, compute (unit_price * quantity).\n"
            "- If user asks 'how many', use COUNT.\n"
            "- If user asks 'value in stock', use SUM(unit_price * quantity_in_stock).\n"
            "- If time periods are mentioned, filter date ranges.\n\n"

            "🔄 Query correction:\n"
            "- If the user input is unclear, infer most likely meaning.\n"
            "- Normalize incorrect spellings.\n\n"

            "📘 Database schema:\n"
            "suppliers(supplier_id, supplier_name, contact_person, phone_number, email, address)\n"
            "pharmacy_inventory(drug_id, drug_name, category, brand, unit_price, quantity_in_stock, expiry_date, supplier_id, reorder_level, location)\n"
            "customers(customer_id, first_name, last_name, phone, email, address)\n"
            "employees(emp_id, emp_name, role, phone, email, salary)\n"
            "sales(sale_id, customer_id, emp_id, sale_date, total_sale)\n"
            "sales_details(sale_detail_id, sale_id, drug_id, quantity, unit_price, subtotal)\n"
            "purchases(purchase_id, supplier_id, emp_id, purchase_date, total_cost)\n"
            "purchase_details(purchase_detail_id, purchase_id, drug_id, quantity, unit_cost, subtotal)\n"
            "doctors(doctor_id, doctor_name, specialization, phone, hospital)\n"
            "prescriptions(prescription_id, doctor_id, customer_id, date_issued, diagnosis)\n\n"
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
            print(f" SQL result data:\n{data}")

            system_message2 = (
                "You are a friendly pharmacy assistant chatbot 🤖💊.\n"
                "You receive structured query results and answer using natural human language.\n\n"

                "🎯 Response Style:\n"
                "- Never mention SQL, queries, tables, or databases.\n"
                "- Format answers using:\n"
                "  • line breaks\n"
                "  • bullet points\n"
                "  • emojis\n"
                "  • **bold labels**\n"
                "- Include drug name, category, brand, price per unit, in-stock quantity, stock value, expiry date, supplier.\n"
                "- If multiple items, list all matching items.\n"
                "- If stock is low, mark with ⚠️.\n"
                "- If empty results, say:\n"
                "  'I couldn’t find anything matching that 😕 Please ask again!'\n"
                "- End with a helpful follow-up question.\n\n"

                "🧮 Perform Calculations:\n"
                "- Total = sum of subtotals.\n"
                "- Compute stock value automatically (unit_price * quantity_in_stock).\n"
                "- Compute percentages if comparison asked.\n\n"

                "📌 Output tone:\n"
                "- Warm, polite, friendly.\n"
                "- Avoid technical language (no SQL, no field names).\n"
            )

            messages2 = [
                SystemMessage(content=system_message2),
                HumanMessage(content=f"User question: {user_query}\n\nSQL result: {data}")
            ]
            llm2 = get_llm(temperature=0.85)
            response2 = llm2.invoke(messages2)
            print(f" Final bot response:\n{response2}")
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
