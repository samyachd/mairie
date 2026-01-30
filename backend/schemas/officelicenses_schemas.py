# schemas/office_licenses.py
from pydantic import BaseModel, Field
from schemas.base_equipment_schemas import BaseEquipmentCreate, BaseEquipmentUpdate, BaseEquipmentRead

# ============= CREATE =============
class OfficeLicenseCreate(BaseEquipmentCreate):
    """Créer une nouvelle licence Office"""
    
    # version est OBLIGATOIRE (contrainte dans ton modèle)
    version: str = Field(..., min_length=1, max_length=500, description="Version d'Office (ex: Office 2021, Microsoft 365)")


# ============= UPDATE =============
class OfficeLicenseUpdate(BaseEquipmentUpdate):
    """Mettre à jour une licence Office (tous les champs optionnels)"""
    
    version: str | None = Field(None, min_length=1, max_length=500)


# ============= READ =============
class OfficeLicenseRead(BaseEquipmentRead):
    """Licence Office complète retournée par l'API"""
    
    version: str
    
    # Si tu veux inclure les ordinateurs qui utilisent cette licence
    # ordinateurs: list["PCReadSimple"] = []  # Liste des PC avec cette licence


# ============= Version simplifiée pour les relations =============
class OfficeLicenseReadSimple(BaseModel):
    """Version simplifiée d'une licence Office (pour les relations)"""
    
    model_config = {"from_attributes": True}
    
    id: int
    version: str
    tag: str | None = None