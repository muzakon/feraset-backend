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
    R2_ACCESS_KEY_ID: str
    R2_SECRET: str
    R2_BUCKET_NAME: str
    R2_API_URL: str
    R2_REGION: str
    R2_PUBLIC_URL: str
    
    # Load Env File
    model_config = SettingsConfigDict(env_file=env_file)


settings = Settings()


@lru_cache
def get_settings() -> Settings:
    return settings
