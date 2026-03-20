from sqlalchemy.orm import Mapped, relationship
from db.models.base import  Document
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.ecran import Ecran
    from db.models.ordinateur import Ordinateur
    from db.models.office_license import OfficeLicense


class Devis(Document):
    __tablename__ = "devis"

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="devis")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="devis")
    office_license: Mapped[list["OfficeLicense"]] = relationship(back_populates="devis")

class BonDeCommande(Document):
    __tablename__ = "bon_de_commande"

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="bon_de_commande")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="bon_de_commande")
    office_license: Mapped[list["OfficeLicense"]] = relationship(back_populates="bon_de_commande")

class Facture(Document):
    __tablename__ = "facture"

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="facture")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="facture")
    office_license: Mapped[list["OfficeLicense"]] = relationship(back_populates="facture")