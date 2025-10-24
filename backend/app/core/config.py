from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    OPENAI_API_KEY: str | None = None
    REDIS_URL: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
