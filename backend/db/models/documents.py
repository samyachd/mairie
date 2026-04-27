from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.models.base import  Document
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from db.models.ecran import Ecran
    from db.models.ordinateur import Ordinateur
    from db.models.office_licence import OfficeLicence

class Devis(Document):
    __tablename__ = "devis"

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="devis")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="devis")
    office_licence: Mapped[list["OfficeLicence"]] = relationship(back_populates="devis")

class BonDeCommande(Document):
    __tablename__ = "bon_de_commande"

    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="bon_de_commande")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="bon_de_commande")
    office_licence: Mapped[list["OfficeLicence"]] = relationship(back_populates="bon_de_commande")

class Facture(Document):
    __tablename__ = "facture"

    montant_ttc: Mapped[float | None] = mapped_column(nullable=True)
    montant_ht: Mapped[float | None] = mapped_column(nullable=True)
    ordinateur: Mapped[list["Ordinateur"]] = relationship(back_populates="facture")
    ecran: Mapped[list["Ecran"]] = relationship(back_populates="facture")
    office_licence: Mapped[list["OfficeLicence"]] = relationship(back_populates="facture")