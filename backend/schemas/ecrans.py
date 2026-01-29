from schemas.base_equipment import BaseEquipment
from datetime import datetime

class EcranBase(BaseEquipment):
    taille: str | None = None

class EcranCreate(EcranBase):
    tag: str

class EcranUpdate(EcranBase):
    pass

class EcranRead(EcranBase):
    id: int
    created_at: datetime | None = None