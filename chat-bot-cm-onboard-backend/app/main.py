from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.chat import router as chat_router
from app.api.routes.session import router as session_router
# from app.core.database import engine, Base
from dotenv import load_dotenv


load_dotenv()


app = FastAPI(
    title="Chatbot API",
    docs_url = "/docs",
    redocs_url = "/redocs",
)




# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create DB tables
# Base.metadata.create_all(bind=engine)


app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(session_router, prefix="/api/session", tags=["session"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Chatbot API running"}