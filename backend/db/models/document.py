from __future__ import annotations
import datetime as dt
from enum import Enum as PyEnum
from sqlalchemy import (
    CheckConstraint,
    Date,
    Enum,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import BaseEntry
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from db.models.ordinateur import Ordinateur
    from db.models.ecran import Ecran
    from db.models.office_licence import OfficeLicence


class DocumentType(str, PyEnum):
    devis = "devis"
    bon_de_commande = "bon_de_commande"
    facture = "facture"


class Document(BaseEntry):
    __tablename__ = "document"

    type: Mapped[DocumentType] = mapped_column(
        Enum(DocumentType, name="document_type_enum"),
        nullable=False,
        index=True,
    )

    nom: Mapped[str] = mapped_column(String(255), nullable=False)
    numero: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    path: Mapped[str] = mapped_column(String(255), nullable=False)
    date_document: Mapped[dt.date] = mapped_column(Date, nullable=False)

    montant_ttc: Mapped[float | None] = mapped_column(Float, nullable=True)
    montant_ht: Mapped[float | None] = mapped_column(Float, nullable=True)

    ordinateur_id: Mapped[int | None] = mapped_column(
        ForeignKey("ordinateur.id", ondelete="SET NULL"), nullable=True, index=True
    )
    ecran_id: Mapped[int | None] = mapped_column(
        ForeignKey("ecran.id", ondelete="SET NULL"), nullable=True, index=True
    )
    office_licence_id: Mapped[int | None] = mapped_column(
        ForeignKey("office_licence.id", ondelete="SET NULL"), nullable=True, index=True
    )

    ordinateur: Mapped[Optional["Ordinateur"]] = relationship(back_populates="documents")
    ecran: Mapped[Optional["Ecran"]] = relationship(back_populates="documents")
    office_licence: Mapped[Optional["OfficeLicence"]] = relationship(
        back_populates="documents"
    )

    __table_args__ = (
        CheckConstraint(
            "(CASE WHEN ordinateur_id IS NOT NULL THEN 1 ELSE 0 END "
            "+ CASE WHEN ecran_id IS NOT NULL THEN 1 ELSE 0 END "
            "+ CASE WHEN office_licence_id IS NOT NULL THEN 1 ELSE 0 END) <= 1",
            name="ck_document_single_owner",
        ),
        CheckConstraint(
            "type = 'facture' OR (montant_ttc IS NULL AND montant_ht IS NULL)",
            name="ck_document_montant_only_facture",
        ),
    )
