from pydantic import BaseModel
from .ordinateur import OrdinateurRead
from .ecran import EcranRead
from .office_licence import OfficeLicenceRead
from .documents import DevisRead, BonDeCommandeRead, FactureRead
from .agent import AgentRead


class InventaireRead(BaseModel):
    ordinateurs: list[OrdinateurRead]
    ecrans: list[EcranRead]
    licences: list[OfficeLicenceRead]
    agents: list[AgentRead]
    devis: list[DevisRead]
    bons_de_commande: list[BonDeCommandeRead]
    factures: list[FactureRead]