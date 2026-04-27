from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict


class OfficeLicenceCreate(BaseModel):
    """Créer une nouvelle licence Office."""
    
    version: str = Field(..., min_length=1, max_length=500)
    type_licence: str | None = Field(None, max_length=255)
    fournisseur: str | None = Field(None, max_length=255)
    date_achat: date
    
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None


class OfficeLicenceUpdate(BaseModel):
    """Mettre à jour une licence Office (tous les champs optionnels)."""
    
    version: str | None = Field(None, min_length=1, max_length=500)
    type_licence: str | None = Field(None, max_length=255)
    fournisseur: str | None = Field(None, max_length=255)
    date_achat: date | None = None
    
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None


class OfficeLicenceRead(BaseModel):
    """Licence Office complète retournée par l'API."""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    version: str
    type_licence: str | None = None
    fournisseur: str | None = None
    date_achat: date
    
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None
    
    created_at: datetime
    updated_at: datetime | None = None