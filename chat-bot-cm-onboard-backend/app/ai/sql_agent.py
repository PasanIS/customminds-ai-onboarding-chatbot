# langchain + SQL logics

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from app.core.database import engine
from app.core.config import settings
from app.ai.llm_manager import get_llm

DATABASE_URL = settings.DATABASE_URL

def get_sql_agent():

    # langchain SQL agent + dynamically generate and execute queries
    db = SQLDatabase.from_uri(DATABASE_URL)
    llm = get_llm()

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )
    return agent_executor