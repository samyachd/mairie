# schemas/__init__.py
"""
Schémas Pydantic pour l'API
"""

from schemas.base_equipment_schemas import (
    BaseEquipmentCreate,
    BaseEquipmentUpdate,
    BaseEquipmentRead,
)

from schemas.ordinateurs_schemas import (
    PCCreate,
    PCUpdate,
    PCRead,
    PCReadSimple,
)

from schemas.ecrans_schemas import (
    EcranCreate,
    EcranUpdate,
    EcranRead,
    EcranReadSimple,
)

from schemas.officelicenses_schemas import (
    OfficeLicenseCreate,
    OfficeLicenseUpdate,
    OfficeLicenseRead,
    OfficeLicenseReadSimple,
)

__all__ = [
    # Base
    "BaseEquipmentCreate",
    "BaseEquipmentUpdate",
    "BaseEquipmentRead",
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