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

from schemas.office_license import (
    OfficeLicenseCreate,
    OfficeLicenseUpdate,
    OfficeLicenseRead,
)

__all__ = [
    # Ordinateurs
    "OrdinateurCreate",
    "OrdinateurUpdate",
    "OrdinateurRead",
    "OrdinateurReadSimple",
    # Écrans
    "EcranCreate",
    "EcranUpdate",
    "EcranRead",
    "EcranReadSimple",
    # Licences Office
    "OfficeLicenseCreate",
    "OfficeLicenseUpdate",
    "OfficeLicenseRead",
    "OfficeLicenseReadSimple",
]