import datetime as dt
from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from db.db import Base

class BaseEntry(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_by: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

class Document(BaseEntry):
    __abstract__ = True

    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(50), nullable=False)
    path: Mapped[str] = mapped_column(String(255), nullable=False)

class BaseEquipement(BaseEntry):
    __abstract__ = True

    proprietaire: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    service: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    batiment: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    type_equipement: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    tag: Mapped[str | None] = mapped_column(String(50), unique=True, nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    date_achat: Mapped[dt.date] = mapped_column(Date, nullable=False)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
