from pydantic_settings import BaseSettings
from pydantic import EmailStr


class Setting(BaseSettings):
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRY: int = 15
    SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ADMIN_EMAIL: EmailStr
    ADMIN_PASSWORD: str
    GROQ_PROVIDER_API_KEY: str
    GROQ_PROVIER_BASE_URL: str = "https://api.groq.com/openai/v1"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_API_KEY: str
    EMBEDDING_MODEL: str = "nvidia/nv-embed-v1"
    CHAT_MODEL_NAME: str = "openai/gpt-oss-20b"
    TAVILY_API: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Setting()
