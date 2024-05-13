import os
from dotenv import load_dotenv
#from pydantic_settings import BaseSettings

env_path = ".env"
load_dotenv(dotenv_path= env_path)

#class Settings(BaseSettings):  # Alternative
class Settings:
    PROJECT_NAME: str = "Within the Box"
    PROJECT_VERSION: str = "0.0.1"

    # Database configuration variables
    POSTGRES_USER : str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER : str = os.getenv("POSTGRES_SERVER","localhost")
    POSTGRES_PORT : str = os.getenv("POSTGRES_PORT",5432) # 5432 is the default postgresql port
    POSTGRES_DB : str = os.getenv("POSTGRES_DB")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

settings = Settings()