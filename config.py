from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

   
    groq_api_key: str = ""
    anthropic_api_key: str = ""

   
    elevenlabs_api_key: str = ""
    tts_provider: str = "gtts"

    
    groq_text_model: str = "llama-3.3-70b-versatile"
    groq_vision_model: str = "llava-v1.5-7b-4096-preview"

    
    app_env: str = "development"
    secret_key: str = "change-this-in-production"

   
    database_url: str = "sqlite+aiosqlite:///./medibot.db"

    
    max_upload_size_mb: int = 10
    upload_dir: str = "uploads/"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",        
    }


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()