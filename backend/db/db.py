from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from core.settings import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,          # True pour debug SQL
    pool_pre_ping=True,  # évite les connexions mortes
)

class Base(DeclarativeBase):
    pass
