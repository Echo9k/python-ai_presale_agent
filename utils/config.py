# utils/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    LANGSMITH_API_KEY: str  # For future use if needed
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
