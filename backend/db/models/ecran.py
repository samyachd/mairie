from __future__ import annotations
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEquipement
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from db.models.agent import Agent
    from db.models.documents import Devis, BonDeCommande, Facture
    from db.models.ordinateur import Ordinateur


class Ecran(BaseEquipement):
    __tablename__ = "ecran"

    ordinateur_id: Mapped[int | None] = mapped_column(ForeignKey("ordinateur.id", ondelete="SET NULL"), nullable=True, index=True)
    agent_id: Mapped[int | None] = mapped_column(ForeignKey("agent.id", ondelete="SET NULL"), nullable=True, index=True)
    devis_id: Mapped[int | None] = mapped_column(ForeignKey("devis.id", ondelete="SET NULL"), nullable=True)
    bon_de_commande_id: Mapped[int | None] = mapped_column(ForeignKey("bon_de_commande.id", ondelete="SET NULL"), nullable=True)
    facture_id: Mapped[int | None] = mapped_column(ForeignKey("facture.id", ondelete="SET NULL"), nullable=True)

    taille: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    slot: Mapped[int | None] = mapped_column(Integer, nullable=True)

    agent: Mapped[Optional["Agent"]] = relationship(back_populates="ecran", passive_deletes=True)
    devis: Mapped[Optional["Devis"]] = relationship(back_populates="ecran")
    bon_de_commande: Mapped[Optional["BonDeCommande"]] = relationship(back_populates="ecran")
    facture: Mapped[Optional["Facture"]] = relationship(back_populates="ecran")
    ordinateur: Mapped[Optional["Ordinateur"]] = relationship(back_populates="ecran")
    __table_args__ = (
        UniqueConstraint("ordinateur_id", "slot", name="uq_ecran_slot_per_pc"),
        CheckConstraint("slot IS NULL OR (slot BETWEEN 1 AND 5)", name="ck_slot_1_5"),
    )