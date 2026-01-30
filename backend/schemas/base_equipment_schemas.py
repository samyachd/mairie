# schemas/base_equipment.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

# ============= SCHÉMA DE CRÉATION (ce que le client ENVOIE) =============
class BaseEquipmentCreate(BaseModel):
    """Champs nécessaires pour créer un équipement"""
    
    # Champs que le CLIENT peut fournir
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
    
    # PAS d'id, created_at, updated_at, created_by, updated_by
    # → Ces champs sont gérés automatiquement par le serveur


# ============= SCHÉMA DE MISE À JOUR (ce que le client ENVOIE) =============
class BaseEquipmentUpdate(BaseModel):
    """Champs modifiables d'un équipement (tous optionnels)"""
    
    # Tous les champs sont optionnels pour permettre des mises à jour partielles
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


# ============= SCHÉMA DE LECTURE (ce que l'API RETOURNE) =============
class BaseEquipmentRead(BaseModel):
    """Représentation complète d'un équipement retourné par l'API"""
    
    model_config = ConfigDict(from_attributes=True)  # Pour convertir depuis SQLAlchemy
    
    # TOUS les champs, y compris ceux générés automatiquement
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
    
    # Optionnel : si tu veux tracker qui a créé/modifié
    # created_by: int | None = None  # ID de l'utilisateur
    # updated_by: int | None = None