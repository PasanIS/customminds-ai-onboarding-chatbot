from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session as DBSession
from app.agent.agent_graph import create_graph
from app.agent.agent_state import AgentState
from app.models.chat_message import ChatMessage
from app.models.session import Session as SessionModel
from langchain.chains import LLMChain

class ChatService:
    def __init__(self, db: DBSession):
        self.db = db
        self.agent = create_graph()

    def validate_session(self, session_id: str):
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID is required")
        session = self.db.query(SessionModel).filter(SessionModel.session_id == session_id).first()
        if not session:
            raise HTTPException(status_code=401, detail="Invalid session")
        if session.expires_at and session.expires_at < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Session expired")

        session.last_active = datetime.utcnow()
        self.db.commit()
        return session


    async def process_message(self, session_id: str, message: str):
        self.validate_session(session_id)

        user_msg = ChatMessage(session_id=session_id, sender="user", content=message)
        self.db.add(user_msg)
        self.db.commit()
        self.db.refresh(user_msg)

        initial_agent_state: AgentState = {
            "messages": [],
            "user_query": message,
            "reply": ""
        }


        agent_state = await self.agent.ainvoke(initial_agent_state)
        response = agent_state["reply"]

        print("Lakmal (state reply):", response)

        bot_msg = ChatMessage(session_id=session_id, sender="bot", content=response)
        self.db.add(bot_msg)
        self.db.commit()
        self.db.refresh(bot_msg)

        return {"reply": response, "saved": True}
