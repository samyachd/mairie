from __future__ import annotations
import datetime as dt
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEntry
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from db.models.documents import Devis, BonDeCommande, Facture
    from db.models.ordinateur import Ordinateur

class OfficeLicence(BaseEntry):
    __tablename__ = "office_licence"

    devis_id: Mapped[int | None] = mapped_column(ForeignKey("devis.id", ondelete="SET NULL"), nullable=True)
    bon_de_commande_id: Mapped[int | None] = mapped_column(ForeignKey("bon_de_commande.id", ondelete="SET NULL"), nullable=True)
    facture_id: Mapped[int | None] = mapped_column(ForeignKey("facture.id", ondelete="SET NULL"), nullable=True)

    type_licence: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    version: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    date_achat: Mapped[dt.date] = mapped_column(Date, nullable=False)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="office_licence", passive_deletes=True)
    devis: Mapped[Optional["Devis"]] = relationship(back_populates="office_licence")
    bon_de_commande: Mapped[Optional["BonDeCommande"]] = relationship(back_populates="office_licence")
    facture: Mapped[Optional["Facture"]] = relationship(back_populates="office_licence")
