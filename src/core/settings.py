from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = ".env"
class Settings(BaseSettings):
    CREATE_WEBHOOK: str
    GCP_PROJECT_ID: str
    QUEUE_NAME: str
    QUEUE_LOCATION: str
    WEBHOOK_URL: str
    COLLECTION_NAME: str
    GCP_BUCKET_NAME: str

    # Load Env File
    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return settings
