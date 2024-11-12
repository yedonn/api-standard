from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement à partir du fichier .env

class Settings(BaseSettings):
    REDIS_URL: str
    DATABASE_URL: str 
    RABBITMQ_URL: str 
    WEBSOCKET_URL: str 
    SERVICE_NAME: str
    SERVICE_URL: str
    APPNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    RABBITMQ_PORT:int
    SERVICE_PORT: int
    CONSUL_HOST: str
    CONSUL_PORT: int
    API_GATEWAY_URL: str
    API_GATEWAY_PORT:int

    class Config:
        env_file = f".env.{os.getenv('ENVIRONMENT', 'development')}"  # Default to .env.development
        extra = "allow"

settings = Settings()
