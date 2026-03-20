from sqlalchemy import String, Enum
from db.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from enum import Enum as PyEnum

class RoleEnum(str, PyEnum):
    admin = "admin"
    user = "user"
    read = "read"

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    mot_de_passe_hash: Mapped[str] = mapped_column(String(500), nullable=False)
    role : Mapped[str] = mapped_column(Enum(RoleEnum), default=RoleEnum.read, nullable=False)