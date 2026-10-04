from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/civicme"
    secret_key: str = "change-this-demo-secret"
    cors_origins: str = "http://localhost:5173"
    upload_dir: str = "/app/uploads"
settings=Settings()
