from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.core.database import get_db
from app.models.chat_message import ChatMessage
from app.services.chatbot_service import generate_reply


router = APIRouter()

@router.post("/api/chat/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):

    try:
        # Save user message
        user_msg = ChatMessage(sender="user", content=request.message)
        db.add(user_msg)
        db.commit()
        db.refresh(user_msg)

        # Generate chatbot reply
        reply_text = await generate_reply(request.message, session_id=request.session_id)

        # Save bot message
        bot_msg = ChatMessage(sender="bot", content=reply_text)
        db.add(bot_msg)
        db.commit()
        db.refresh(bot_msg)

        return ChatResponse(reply=reply_text, saved=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))