from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session as DBSession
from app.core.database import get_db
from app.schemas.chat_schema import ChatRequest, ChatResponse, ChatMessageOut
from app.services.chatbot_service import ChatService
from app.services.session_services import SessionService
from app.schemas.session import SessionCreate

router = APIRouter(prefix="/api/chat/start", tags=["Chat"])

@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest, fastapi_request: Request, db: DBSession = Depends(get_db)):
    chat_service = ChatService(db)
    session_service = SessionService(db)

    try:
        session_id = request.session_id
        if not session_id:

            ip_address = fastapi_request.client.host if fastapi_request.client else None
            user_agent = fastapi_request.headers.get("user-agent")
            session_data = SessionCreate(ip_address=ip_address, user_agent=user_agent)
            new_session = session_service.create_session(session_data)
            session_id = new_session.session_id

        if not session_service.is_session_valid(session_id):
            raise HTTPException(status_code=401, detail="Invalid or expired session")

        result = await chat_service.process_message(session_id, request.message)

        bot_msg = result.get("message")
        chat_message_out = ChatMessageOut.from_orm(bot_msg) if bot_msg is not None else None

        return ChatResponse(reply=result["reply"], saved=result["saved"], message=chat_message_out, session_id=session_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
