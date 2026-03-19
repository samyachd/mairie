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
    PCCreate,
    PCUpdate,
    PCRead,
)

from schemas.ecran import (
    EcranCreate,
    EcranUpdate,
    EcranRead,
)

from backend.schemas.office_license import (
    OfficeLicenseCreate,
    OfficeLicenseUpdate,
    OfficeLicenseRead,
)

__all__ = [
    # Ordinateurs
    "PCCreate",
    "PCUpdate",
    "PCRead",
    "PCReadSimple",
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