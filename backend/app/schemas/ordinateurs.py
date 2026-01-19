from pydantic import BaseModel, IPvAnyAddress, ConfigDict
from datetime import datetime, date

class PCBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type_pc: str | None = None
    marque: str | None = None
    proprietaire: str | None = None
    service: str | None = None
    batiment: str | None = None
    fournisseur: str | None = None
    os: str | None = None
    tag: str | None = None
    nom_reseau: str | None = None
    ram: str | None = None
    tag_chargeur: str | None = None
    numero_bc: str | None = None
    ip_address: IPvAnyAddress | None = None
    mac_ethernet: str | None = None
    mac_wifi: str | None = None
    watt: int | None = None
    fin_garantie: date | None = None
    achat: date | None = None
    clef_wifi: bool | None = None
    lecteur_cd: bool | None = None
    casque: bool | None = None
    absolute_dell: bool | None = None

class PCCreate(PCBase):
    tag: str

class PCUpdate(PCBase):
    pass

class PCRead(PCBase):
    id: int
    created_at: datetime | None = None