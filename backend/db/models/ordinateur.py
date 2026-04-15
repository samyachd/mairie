from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEquipement
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from db.models.ecran import Ecran
    from db.models.agent import Agent
    from db.models.documents import Devis, BonDeCommande, Facture
    from db.models.office_licence import OfficeLicence

class Ordinateur(BaseEquipement):
    __tablename__ = "ordinateur"

    officelicence_id: Mapped[int | None] = mapped_column(ForeignKey("officelicence.id", ondelete="SET NULL"), nullable=True, index=True)
    devis_id: Mapped[int | None] = mapped_column(ForeignKey("devis.id", ondelete="SET NULL"), nullable=True)
    bon_de_commande_id: Mapped[int | None] = mapped_column(ForeignKey("bon_de_commande.id", ondelete="SET NULL"), nullable=True)
    facture_id: Mapped[int | None] = mapped_column(ForeignKey("facture.id", ondelete="SET NULL"), nullable=True)

    ram: Mapped[str | None] = mapped_column(String(50), nullable=True)
    os: Mapped[str | None] = mapped_column(String(100), nullable=True)
    nom_reseau: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    tag_chargeur: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True, unique=True)
    mac_ethernet: Mapped[str | None] = mapped_column(String(17), nullable=True, unique=True)
    mac_wifi: Mapped[str | None] = mapped_column(String(17), nullable=True, unique=True)
    clef_wifi: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    lecteur_cd: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    casque: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    absolute_dell: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    watt: Mapped[int | None] = mapped_column(Integer, nullable=True)

    ecran: Mapped[Optional[list["Ecran"]]] = relationship(back_populates="ordinateur", passive_deletes=True)
    officelicence: Mapped[Optional["OfficeLicence"]] = relationship(back_populates="ordinateur", passive_deletes=True)
    agent: Mapped[Optional["Agent"]] = relationship(back_populates="ordinateur", passive_deletes=True)
    devis: Mapped[Optional["Devis"]] = relationship(back_populates="ordinateur")
    bon_de_commande: Mapped[Optional["BonDeCommande"]] = relationship(back_populates="ordinateur")
    facture: Mapped[Optional["Facture"]] = relationship(back_populates="ordinateur")
