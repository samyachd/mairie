import os
from sqlalchemy.engine import URL
from dotenv import load_dotenv

load_dotenv()


load_dotenv(override=True)  # important

print("DB_USER:", os.getenv("DB_USER"))
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))

db_pass = os.getenv("DB_PASS")
print("DB_PASS:", db_pass)
print("DB_PASS present?", db_pass is not None)
print("DB_PASS length:", len(db_pass) if db_pass else None)
print("DB_PASS startswith:", db_pass[:2] if db_pass else None)  # 2 chars max

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
