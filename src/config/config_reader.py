from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    OWNER_CODE: str
    ADMIN_ID: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

settings = Settings()