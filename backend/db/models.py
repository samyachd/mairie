from __future__ import annotations
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime as dt
from .db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, index=True, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Ordinateurs(Base):
    __tablename__ = "ordinateurs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    ecran_01_id: Mapped[int | None] = mapped_column(ForeignKey("ecrans01.id", ondelete="SET NULL"), nullable=True)
    ecran_02_id: Mapped[int | None] = mapped_column(ForeignKey("ecrans02.id", ondelete="SET NULL"), nullable=True)
    ecran_03_id: Mapped[int | None] = mapped_column(ForeignKey("ecrans03.id", ondelete="SET NULL"), nullable=True)
    ecran_04_id: Mapped[int | None] = mapped_column(ForeignKey("ecrans04.id", ondelete="SET NULL"), nullable=True)
    ecran_05_id: Mapped[int | None] = mapped_column(ForeignKey("ecrans05.id", ondelete="SET NULL"), nullable=True)
    office_license_id: Mapped[int | None] = mapped_column(ForeignKey("office_licenses.id", ondelete="SET NULL"), nullable=True)

    proprietaire: Mapped[str | None] = mapped_column(String(255), nullable=True)
    service: Mapped[str | None] = mapped_column(String(255), nullable=True)
    batiment: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type_pc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)

    os: Mapped[str | None] = mapped_column(String(100), nullable=True)

    tag: Mapped[str | None] = mapped_column(String(50), nullable=True)
    nom_reseau: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ram: Mapped[str | None] = mapped_column(String(50), nullable=True)
    tag_chargeur: Mapped[str | None] = mapped_column(String(50), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    mac_ethernet: Mapped[str | None] = mapped_column(String(17), nullable=True)
    mac_wifi: Mapped[str | None] = mapped_column(String(17), nullable=True)

    clef_wifi: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    lecteur_cd: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    casque: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    absolute_dell: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    watt: Mapped[int | None] = mapped_column(Integer, nullable=True)

    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User | None] = relationship(back_populates="ordinateurs")
    ecran_01: Mapped[Ecrans01 | None] = relationship(back_populates="ordinateurs")
    ecran_02: Mapped[Ecrans02 | None] = relationship(back_populates="ordinateurs")
    ecran_03: Mapped[Ecrans03 | None] = relationship(back_populates="ordinateurs")
    ecran_04: Mapped[Ecrans04 | None] = relationship(back_populates="ordinateurs")
    ecran_05: Mapped[Ecrans05 | None] = relationship(back_populates="ordinateurs")
    office_license: Mapped[OfficeLicenses | None] = relationship(back_populates="ordinateurs")

class Ecrans01(Base):
    __tablename__ = "ecrans01"

    id: Mapped[int] = mapped_column(primary_key=True)
    taille: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="ecran_01")

class Ecrans02(Base):
    __tablename__ = "ecrans02"

    id: Mapped[int] = mapped_column(primary_key=True)
    taille: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="ecran_02")

class Ecrans03(Base):
    __tablename__ = "ecrans03"

    id: Mapped[int] = mapped_column(primary_key=True)
    taille: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="ecran_03")

class Ecrans04(Base):
    __tablename__ = "ecrans04"

    id: Mapped[int] = mapped_column(primary_key=True)
    taille: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="ecran_04")

class Ecrans05(Base):
    __tablename__ = "ecrans05"

    id: Mapped[int] = mapped_column(primary_key=True)
    taille: Mapped[str | None] = mapped_column(String(255), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tag: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="ecran_05")

class OfficeLicenses(Base):
    __tablename__ = "office_licenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    version: Mapped[str | None] = mapped_column(String(500), nullable=True)
    type_license: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="office_license")
