from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

class EcranBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    tag: str | None = None
    achat: date | None = None
    fin_garantie: date | None = None
    numero_bc: str | None = None
    taille: str | None = None
    marque: str | None = None
    modele: str | None = None
    fournisseur: str | None = None

class EcranCreate(EcranBase):
    tag: str

class EcranUpdate(EcranBase):
    pass

class EcranRead(EcranBase):
    id: int
    created_at: datetime | None = None