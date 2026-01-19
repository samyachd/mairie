from pydantic import BaseModel, ConfigDict
from datetime import datetime, date

class LicenseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    achat: date | None = None
    numero_bc: str | None = None
    version: str | None = None
    type_license: str | None = None
    
class LicenseCreate(LicenseBase):
    version: str

class LicenseUpdate(LicenseBase):
    pass

class LicenseRead(LicenseBase):
    id: int
    created_at: datetime | None = None