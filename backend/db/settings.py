import os
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = int(os.environ.get("DB_PORT", 5432))  # ← ICI
    DB_NAME = os.environ["DB_NAME"]

    DATABASE_URL = URL.create(
        drivername="postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

settings = Settings()

print(settings.DATABASE_URL)
print(type(settings.DATABASE_URL))
