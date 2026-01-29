from schemas.base_equipment import BaseEquipment
from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

class PCBase(BaseEquipment):
    os: str | None = None
    tag: str | None = None
    nom_reseau: str | None = None
    ram: str | None = None
    tag_chargeur: str | None = None
    ip_address: str| None = None
    mac_ethernet: str | None = None
    mac_wifi: str | None = None
    watt: int | None = None
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