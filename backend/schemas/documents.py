from pydantic import BaseModel
from datetime import datetime

class FactureResponse(BaseModel):
    id: int
    equipement_id: int
    fournisseur: str | None
    montant: float | None
    date_facture: datetime | None
    numero_facture: str | None
    date_ajout: datetime

    class Config:
        from_attributes = True

class DevisResponse(BaseModel):
    id: int
    equipement_id: int
    fournisseur: str | None
    montant: float | None
    date_devis: datetime | None
    date_ajout: datetime

    class Config:
        from_attributes = True

class BonDeCommandeResponse(BaseModel):
    id: int
    equipement_id: int
    fournisseur: str | None
    montant: float | None
    date_bon: datetime | None
    date_ajout: datetime

    class Config:
        from_attributes = True

class DocumentsResponse(BaseModel):
    factures: list[FactureResponse]
    devis: list[DevisResponse]
    bons_de_commande: list[BonDeCommandeResponse]