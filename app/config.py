from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "sqlite:///./test.db"

  # read connection info from environment variables
    DB_HOST: str
    DB_NAME: str
    DB_USER: str 
    DB_PASSWORD: str 
    DB_PORT: str 
    # JWT settings
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    class Config:
        env_file = ".env"


settings = Settings()