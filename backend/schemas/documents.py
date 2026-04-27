from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


# ──────────────────────────────────────────────────────
# Base : champs communs aux 3 types de documents
# ──────────────────────────────────────────────────────

class DocumentBase(BaseModel):
    """Champs communs à Devis, BonDeCommande et Facture."""
    
    nom: str = Field(..., min_length=1, max_length=255)
    numero: str = Field(..., min_length=1, max_length=50)
    path: str = Field(..., min_length=1, max_length=255)
    date_document: date


class DocumentRead(BaseModel):
    """Champs lus communs aux 3 types de documents."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    nom: str
    numero: str
    path: str
    date_document: date
    created_at: datetime
    updated_at: datetime | None = None


# ──────────────────────────────────────────────────────
# Devis
# ──────────────────────────────────────────────────────

class DevisCreate(DocumentBase):
    pass


class DevisUpdate(BaseModel):
    nom: str | None = Field(None, min_length=1, max_length=255)
    numero: str | None = Field(None, min_length=1, max_length=50)
    path: str | None = Field(None, min_length=1, max_length=255)
    date_document: date | None = None


class DevisRead(DocumentRead):
    pass


# ──────────────────────────────────────────────────────
# Bon de commande
# ──────────────────────────────────────────────────────

class BonDeCommandeCreate(DocumentBase):
    pass


class BonDeCommandeUpdate(BaseModel):
    nom: str | None = Field(None, min_length=1, max_length=255)
    numero: str | None = Field(None, min_length=1, max_length=50)
    path: str | None = Field(None, min_length=1, max_length=255)
    date_document: date | None = None


class BonDeCommandeRead(DocumentRead):
    pass


# ──────────────────────────────────────────────────────
# Facture (avec ses champs spécifiques)
# ──────────────────────────────────────────────────────

class FactureCreate(DocumentBase):
    montant_ttc: float | None = Field(None, ge=0)
    montant_ht: float | None = Field(None, ge=0)


class FactureUpdate(BaseModel):
    nom: str | None = Field(None, min_length=1, max_length=255)
    numero: str | None = Field(None, min_length=1, max_length=50)
    path: str | None = Field(None, min_length=1, max_length=255)
    date_document: date | None = None
    montant_ttc: float | None = Field(None, ge=0)
    montant_ht: float | None = Field(None, ge=0)


class FactureRead(DocumentRead):
    montant_ttc: float | None = None
    montant_ht: float | None = None