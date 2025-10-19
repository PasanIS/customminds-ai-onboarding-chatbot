from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "Chatbot API"
    APP_ENV: str = Field(default="development")
    DATABASE_URL: str
    OPENAI_API_KEY: str
    SESSION_EXPIRE_HOURS: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()