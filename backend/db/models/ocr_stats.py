from __future__ import annotations
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.db import Base

class OcrStat(Base):
    __tablename__ = "ocr_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now(datetime.timezone.utc))

    # Performance
    duree_ms: Mapped[int]          # temps de traitement total
    duree_ocr_ms: Mapped[int]      # temps OCR Mistral seul
    duree_extraction_ms: Mapped[int] # temps extraction JSON

    # Qualité
    succes: Mapped[bool]           # OCR réussi ou non
    nb_champs_extraits: Mapped[int] # nombre de champs trouvés
    nb_champs_vides: Mapped[int]    # champs non trouvés
    taux_completude: Mapped[float]  # % champs remplis

    # Contexte
    type_document: Mapped[str]     # "facture", "devis", "bon_commande"
    type_mime: Mapped[str]         # "application/pdf", "image/jpeg"
    taille_fichier: Mapped[int]    # en bytes
    nb_pages: Mapped[int]          # nombre de pages traitées