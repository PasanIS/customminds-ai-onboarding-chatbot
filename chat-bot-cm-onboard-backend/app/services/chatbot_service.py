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

    async def get_chat_history(self, session_id: str, db: DBSession ):
        messages = (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(10)
            .all()
        )
        return list(reversed(messages))

    async def process_message(self, session_id: str, message: str):
        self.validate_session(session_id)

        user_msg = ChatMessage(session_id=session_id, sender="user", content=message)
        self.db.add(user_msg)
        self.db.commit()
        self.db.refresh(user_msg)

        thread_config = {
            "configurable": {
                "thread_id": session_id,
                "checkpoint_ns": "default"
            }
        }

        messages = await self.get_chat_history(session_id, self.db)

        formatted_messages = [
            {
                "role": "user" if m.sender == "user" else "assistant",
                "content": m.content
            }
            for m in messages
        ]

        initial_agent_state: AgentState = {
            "messages": formatted_messages,
            "user_query": message,
            "reply": "",
            "decision": ""
        }


        agent_state = await self.agent.ainvoke(initial_agent_state, config=thread_config)
        response = agent_state["reply"]

        bot_msg = ChatMessage(session_id=session_id, sender="bot", content=response)
        self.db.add(bot_msg)
        self.db.commit()
        self.db.refresh(bot_msg)

        return {"reply": response, "saved": True}
