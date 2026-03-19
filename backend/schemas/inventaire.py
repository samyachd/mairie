from ordinateur import OrdinateurRead
from ecran import EcranRead
from office_license import OfficeLicenseRead
from pydantic import BaseModel


class InventaireRead(BaseModel):
    ordinateurs: list[OrdinateurRead]
    ecrans: list[EcranRead]
    licenses: list[OfficeLicenseRead]