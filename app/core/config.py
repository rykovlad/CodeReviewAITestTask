import os

from pydantic.v1 import BaseSettings, Field


class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field("your secret key in .env", env="OPENAI_API_KEY")
    GITHUB_API_KEY: str = Field("your secret key in .env", env="GITHUB_API_KEY")
    REDIS_URL: str = "redis://localhost:6379/0"
    API_VERSION: str = "v1"

    class Config:
        env_file =  os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")

config = Settings()
