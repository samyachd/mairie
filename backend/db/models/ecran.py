from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEquipement
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from db.models.agent import Agent
    from db.models.document import Document
    from db.models.ordinateur import Ordinateur


class Ecran(BaseEquipement):
    __tablename__ = "ecran"

    ordinateur_id: Mapped[int | None] = mapped_column(ForeignKey("ordinateur.id", ondelete="SET NULL"), nullable=True, index=True)
    agent_id: Mapped[int | None] = mapped_column(ForeignKey("agent.id", ondelete="SET NULL"), nullable=True, index=True)

    taille: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    slot: Mapped[int | None] = mapped_column(Integer, nullable=True)

    agent: Mapped[Optional["Agent"]] = relationship(back_populates="ecran", passive_deletes=True)
    ordinateur: Mapped[Optional["Ordinateur"]] = relationship(back_populates="ecran")
    documents: Mapped[list["Document"]] = relationship(back_populates="ecran", passive_deletes=True)

    __table_args__ = (
        UniqueConstraint("ordinateur_id", "slot", name="uq_ecran_slot_per_pc"),
        CheckConstraint("slot IS NULL OR (slot BETWEEN 1 AND 5)", name="ck_slot_1_5"),
        CheckConstraint("ordinateur_id IS NULL OR slot IS NOT NULL", name="ck_slot_required_when_linked"),
    )
