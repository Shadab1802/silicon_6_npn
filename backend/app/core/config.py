from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    aws_access_key: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
