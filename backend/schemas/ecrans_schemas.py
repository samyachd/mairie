# schemas/ecrans.py
from pydantic import BaseModel, Field, field_validator
from schemas.base_equipment_schemas import BaseEquipmentCreate, BaseEquipmentUpdate, BaseEquipmentRead

# ============= CREATE =============
class EcranCreate(BaseEquipmentCreate):
    """Créer un nouvel écran"""
    
    # tag est OBLIGATOIRE pour les écrans (contrainte dans ton modèle)
    tag: str = Field(..., min_length=1, max_length=255, description="Tag unique de l'écran")
    
    # Attributs spécifiques aux écrans
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


# ============= UPDATE =============
class EcranUpdate(BaseEquipmentUpdate):
    """Mettre à jour un écran (tous les champs optionnels)"""
    
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


# ============= READ =============
class EcranRead(BaseEquipmentRead):
    """Écran complet retourné par l'API"""
    
    tag: str
    taille: str | None = None
    ordinateur_id: int | None = None
    slot: int | None = None
    
    # Si tu veux inclure l'ordinateur auquel l'écran est connecté
    # ordinateur: "PCReadSimple" | None = None  # Version simplifiée pour éviter la récursion


# ============= Version simplifiée pour les relations =============
class EcranReadSimple(BaseModel):
    """Version simplifiée d'un écran (pour éviter la récursion dans les relations)"""
    
    model_config = {"from_attributes": True}
    
    id: int
    tag: str
    taille: str | None = None
    marque: str | None = None
    slot: int | None = None