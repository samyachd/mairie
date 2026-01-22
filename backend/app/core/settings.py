from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    APP_NAME: str = "Inventaire"
    VERSION: str = "0.1.0"
    DEBUG: bool = False

    DB_USER: str
    DB_PASS: str
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_NAME: str

    @property
    def DATABASE_URL(self) -> URL:
        return URL.create(
            "postgresql+psycopg2",
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
