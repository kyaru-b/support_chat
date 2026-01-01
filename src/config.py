import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str

    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

settings = Settings()
