from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from backend.core.settings import settings

DATABASE_URL = settings.DATABASE_URL
# Pour SQLite: "sqlite:///./app.db" (et ajouter connect_args plus bas)

engine = create_engine(
    DATABASE_URL,
    echo=False,          # True pour debug SQL
    pool_pre_ping=True,  # évite les connexions mortes
)

class Base(DeclarativeBase):
    pass
