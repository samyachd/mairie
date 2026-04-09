from datetime import date
from pydantic import BaseModel, Field

class OfficeLicenceCreate(BaseModel):
    """Créer une nouvelle licence Office"""

    version: str = Field(..., min_length=1, max_length=500, description="Version d'Office (ex: Office 2021, Microsoft 365)")
    type_licence: str | None = Field(None, min_length=1, max_length=255, description="Type de licence Office")
    numero_bc: str = Field(..., min_length=1, max_length=50, description="Numéro de bon de commande")
    achat: date = Field(..., description="Date d'achat")

class OfficeLicenceUpdate(BaseModel):
    """Mettre à jour une licence Office (tous les champs optionnels)"""
    
    version: str | None = Field(None, min_length=1, max_length=500)
    type_licence: str | None = Field(None, min_length=1, max_length=255, description="Type de licence Office")
    numero_bc: str = Field(..., min_length=1, max_length=50, description="Numéro de bon de commande")
    achat: date = Field(..., description="Date d'achat")

class OfficeLicenceRead(BaseModel):
    """Licence Office complète retournée par l'API"""
    
    id : int
    version: str
    type_licence: str | None = Field(None, min_length=1, max_length=255, description="Type de licence Office")
    numero_bc: str = Field(..., min_length=1, max_length=50, description="Numéro de bon de commande")
    achat: date = Field(..., description="Date d'achat")
