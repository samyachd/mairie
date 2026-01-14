import os
from dotenv import load_dotenv, find_dotenv
import psycopg2

load_dotenv(find_dotenv(usecwd=True), override=True)

conn = psycopg2.connect(
    host=os.getenv("DB_HOST","127.0.0.1"),
    port=os.getenv("DB_PORT","5432"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    dbname=os.getenv("DB_NAME"),
)
print("OK psycopg2")
conn.close()
