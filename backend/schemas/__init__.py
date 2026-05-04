"""Pydantic schemas for the API."""

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
    DocumentCreate,
    DocumentUpdate,
    DocumentRead,
)

from schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate,
)

from schemas.auth import Token

from schemas.inventaire import InventaireRead

__all__ = [
    "OrdinateurCreate",
    "OrdinateurUpdate",
    "OrdinateurRead",
    "EcranCreate",
    "EcranUpdate",
    "EcranRead",
    "OfficeLicenceCreate",
    "OfficeLicenceUpdate",
    "OfficeLicenceRead",
    "AgentCreate",
    "AgentUpdate",
    "AgentRead",
    "DocumentCreate",
    "DocumentUpdate",
    "DocumentRead",
    "UserCreate",
    "UserRead",
    "UserUpdate",
    "Token",
    "InventaireRead",
]
