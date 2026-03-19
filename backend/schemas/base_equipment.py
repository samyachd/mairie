from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

class BaseEquipmentCreate(BaseModel):
    """Champs nécessaires pour créer un équipement"""
    
    proprietaire: str | None = None
    service: str | None = None
    batiment: str | None = None
    type_equipement: str | None = None
    fournisseur: str | None = None
    agent: str | None = None
    tag: str | None = None
    marque: str | None = None
    numero_bc: str | None = None
    fin_garantie: date | None = None
    achat: date | None = None

class BaseEquipmentUpdate(BaseModel):
    """Champs modifiables d'un équipement (tous optionnels)"""
    
    proprietaire: str | None = None
    service: str | None = None
    batiment: str | None = None
    type_equipement: str | None = None
    fournisseur: str | None = None
    agent: str | None = None
    tag: str | None = None
    marque: str | None = None
    numero_bc: str | None = None
    fin_garantie: date | None = None
    achat: date | None = None

class BaseEquipmentRead(BaseModel):
    """Représentation complète d'un équipement retourné par l'API"""
    
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    proprietaire: str | None = None
    service: str | None = None
    batiment: str | None = None
    type_equipement: str | None = None
    fournisseur: str | None = None
    agent: str | None = None
    tag: str | None = None
    marque: str | None = None
    numero_bc: str | None = None
    fin_garantie: date | None = None
    achat: date | None = None
    created_at: datetime
    updated_at: datetime | None = None
    
    created_by: int | None = None
    updated_by: int | None = None