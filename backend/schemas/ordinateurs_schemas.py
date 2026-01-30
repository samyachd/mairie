# schemas/ordinateurs.py
from datetime import date
from pydantic import BaseModel, Field
from schemas.base_equipment_schemas import BaseEquipmentCreate, BaseEquipmentUpdate, BaseEquipmentRead

class BaseEquipmentCreate(BaseModel):
    # ========== OBLIGATOIRES ==========
    tag: str = Field(..., min_length=1, max_length=50)
    marque: str = Field(..., min_length=1, max_length=255)
    numero_bc: str = Field(..., min_length=1, max_length=50)
    achat: date
    proprietaire: str | None = None
    service: str | None = None
    batiment: str | None = None 
    type_equipement: str | None = None
    fournisseur: str | None = None
    agent: str | None = None
    fin_garantie: date | None = None



# ============= UPDATE =============
class PCUpdate(BaseEquipmentUpdate):
    """Mettre à jour un ordinateur (tous les champs optionnels)"""
    
    office_license_id: int | None = None
    ram: str | None = Field(None, max_length=50)
    os: str | None = Field(None, max_length=100)
    nom_reseau: str | None = Field(None, max_length=50)
    tag_chargeur: str | None = Field(None, max_length=50)
    ip_address: str | None = Field(None, max_length=45)
    mac_ethernet: str | None = Field(None, max_length=17)
    mac_wifi: str | None = Field(None, max_length=17)
    clef_wifi: bool | None = None
    lecteur_cd: bool | None = None
    casque: bool | None = None
    absolute_dell: bool | None = None
    watt: int | None = Field(None, ge=0)


# ============= READ =============
class PCRead(BaseEquipmentRead):
    """Ordinateur complet retourné par l'API"""
    
    office_license_id: int | None = None
    ram: str | None = None
    os: str | None = None
    nom_reseau: str | None = None
    tag_chargeur: str | None = None
    ip_address: str | None = None
    mac_ethernet: str | None = None
    mac_wifi: str | None = None
    clef_wifi: bool | None = None
    lecteur_cd: bool | None = None
    casque: bool | None = None
    absolute_dell: bool | None = None
    watt: int | None = None
    
    # Relations (optionnel)
    # ecran: list["EcranReadSimple"] = []
    # office_license: "OfficeLicenseReadSimple" | None = None


# ============= Version simplifiée pour les relations =============
class PCReadSimple(BaseModel):
    """Version simplifiée d'un ordinateur (pour éviter la récursion)"""
    
    model_config = {"from_attributes": True}
    
    id: int
    tag: str | None = None
    marque: str | None = None
    nom_reseau: str | None = None
    agent: str | None = None