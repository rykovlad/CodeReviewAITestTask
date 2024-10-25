import os

from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field("your secret key in .env", env="OPENAI_API_KEY")
    GITHUB_API_KEY: str = Field("your secret key in .env", env="GITHUB_API_KEY")

    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_TIME_TO_STORE_CACHE = 60
    API_VERSION: str = "v1"
    CHAT_GPT_MODEL: str = "gpt-4-turbo"

    class Config:
        env_file =  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

config = Settings()
