# backend/app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    aws_access_key: str
    aws_secret_access_key: str
    aws_region: str

    class Config:
        env_file = ".env"

settings = Settings()
