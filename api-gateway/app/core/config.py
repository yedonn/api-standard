from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str
    RABBITMQ_URL: str
    WEBSOCKET_URL: str
    SERVICE_NAME: str
    SERVICE_URL: str
    APPNAME: str
    SERVICE_PORT: int
    RATE_LIMIT_PER_MINUTE: int
    REFRESH_SECRET_KEY: str
    CONSUL_HOST: str
    CONSUL_PORT: int
    

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"  # Default to .env.development
        extra = "allow"

settings = Settings()
