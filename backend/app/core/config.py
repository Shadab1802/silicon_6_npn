from pydantic import BaseSettings, Field
from typing import Optional

class Settings(BaseSettings):
    aws_access_key: Optional[str] = Field(None, env="AWS_ACCESS_KEY")
    aws_secret_access_key: Optional[str] = Field(None, env="AWS_SECRET_ACCESS_KEY")
    aws_region: Optional[str] = Field(None, env="AWS_REGION")
    bucket_name: Optional[str] = Field(None, env="BUCKET_NAME")

    class Config:
        env_file = ".env"

settings = Settings()
