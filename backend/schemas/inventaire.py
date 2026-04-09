from .ordinateur import OrdinateurRead
from .ecran import EcranRead
from .office_licence import OfficeLicenceRead
from .documents import DevisResponse, BonDeCommandeResponse, FactureResponse
from pydantic import BaseModel

class InventaireRead(BaseModel):
    ordinateurs: list[OrdinateurRead]
    ecrans: list[EcranRead]
    licenses: list[OfficeLicenceRead]
    devis: list[DevisResponse]
    bons_de_commande: list[BonDeCommandeResponse]
    factures: list[FactureResponse]