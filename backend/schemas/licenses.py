from schemas.base_equipment import BaseEquipment
from datetime import datetime

class LicenseBase(BaseEquipment):
    version: str | None = None
    
class LicenseCreate(LicenseBase):
    version: str

class LicenseUpdate(LicenseBase):
    pass

class LicenseRead(LicenseBase):
    id: int