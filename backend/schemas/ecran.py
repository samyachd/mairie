from pydantic import Field, field_validator
from schemas.base_equipment import BaseEquipmentCreate, BaseEquipmentUpdate, BaseEquipmentRead

class EcranCreate(BaseEquipmentCreate):
    
    tag: str = Field(..., min_length=1, max_length=255, description="Tag unique de l'écran")
    taille: str | None = Field(None, max_length=255, description="Taille de l'écran (ex: 27 pouces)")
    ordinateur_id: int | None = Field(None, description="ID de l'ordinateur auquel l'écran est connecté")
    slot: int | None = Field(None, ge=1, le=5, description="Numéro du slot (1-5)")
    
    @field_validator('slot')
    @classmethod
    def validate_slot(cls, v):
        """Valider que le slot est entre 1 et 5 (ou None)"""
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Le slot doit être entre 1 et 5')
        return v

class EcranUpdate(BaseEquipmentUpdate):
    
    tag: str | None = Field(None, min_length=1, max_length=255)
    taille: str | None = Field(None, max_length=255)
    ordinateur_id: int | None = None
    slot: int | None = Field(None, ge=1, le=5)
    
    @field_validator('slot')
    @classmethod
    def validate_slot(cls, v):
        if v is not None and (v < 1 or v > 5):
            raise ValueError('Le slot doit être entre 1 et 5')
        return v

class EcranRead(BaseEquipmentRead):
    
    tag: str
    taille: str | None = None
    ordinateur_id: int | None = None
    slot: int | None = None