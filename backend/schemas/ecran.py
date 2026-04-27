from pydantic import Field, field_validator
from schemas.base_equipment import (
    BaseEquipmentCreate,
    BaseEquipmentUpdate,
    BaseEquipmentRead,
)


class EcranCreate(BaseEquipmentCreate):
    """Créer un écran."""
    
    taille: str | None = Field(None, max_length=255)
    slot: int | None = Field(None, ge=1, le=5)
    
    ordinateur_id: int | None = None
    agent_id: int | None = None
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None
    
    @field_validator("slot")
    @classmethod
    def validate_slot(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Le slot doit être entre 1 et 5")
        return v


class EcranUpdate(BaseEquipmentUpdate):
    """Mettre à jour un écran (tous champs optionnels)."""
    
    taille: str | None = Field(None, max_length=255)
    slot: int | None = Field(None, ge=1, le=5)
    
    ordinateur_id: int | None = None
    agent_id: int | None = None
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None
    
    @field_validator("slot")
    @classmethod
    def validate_slot(cls, v: int | None) -> int | None:
        if v is not None and not (1 <= v <= 5):
            raise ValueError("Le slot doit être entre 1 et 5")
        return v


class EcranRead(BaseEquipmentRead):
    """Écran retourné par l'API."""
    
    taille: str | None = None
    slot: int | None = None
    
    ordinateur_id: int | None = None
    agent_id: int | None = None
    devis_id: int | None = None
    bon_de_commande_id: int | None = None
    facture_id: int | None = None