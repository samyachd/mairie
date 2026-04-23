from __future__ import annotations
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEntry
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    
    from db.models.ecran import Ecran
    from db.models.ordinateur import Ordinateur


class Agent(BaseEntry):
    __tablename__ = "agent"

    ordinateur_id: Mapped[int | None] = mapped_column(ForeignKey("ordinateur.id", ondelete="SET NULL"), nullable=True)

    nom: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    prenom: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    service: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True, unique=True, index=True)
    telephone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    ordinateur: Mapped[Optional["Ordinateur"]] = relationship(back_populates="agent", passive_deletes=True)
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="agent", passive_deletes=True)