# schemas/__init__.py
"""
Schémas Pydantic pour l'API
"""

from schemas.base_equipment import (
    BaseEquipmentCreate,
    BaseEquipmentUpdate,
    BaseEquipmentRead,
)

from schemas.ordinateur import (
    OrdinateurCreate,
    OrdinateurUpdate,
    OrdinateurRead,
)

from schemas.ecran import (
    EcranCreate,
    EcranUpdate,
    EcranRead,
)

from schemas.office_licence import (
    OfficeLicenceCreate,
    OfficeLicenceUpdate,
    OfficeLicenceRead,
)

from schemas.agent import (
    AgentCreate,
    AgentUpdate,
    AgentRead,
)

from schemas.documents import (
    DevisResponse,
    FactureResponse,
    BonDeCommandeResponse,
)

from schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)

from schemas.auth import (
    Token,
)

from schemas.inventaire import InventaireRead

__all__ = [
    # Ordinateurs
    "OrdinateurCreate",
    "OrdinateurUpdate",
    "OrdinateurRead",
    # Écrans
    "EcranCreate",
    "EcranUpdate",
    "EcranRead",
    # Licences Office
    "OfficeLicenceCreate",
    "OfficeLicenceUpdate",
    "OfficeLicenceRead",
    # Agents
    "AgentCreate",
    "AgentUpdate",
    "AgentRead",
    # Documents
    "DevisResponse",
    "FactureResponse",
    "BonDeCommandeResponse",
]