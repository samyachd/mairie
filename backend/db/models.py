from __future__ import annotations
from typing import Optional
from sqlalchemy import CheckConstraint, String, Integer, ForeignKey, DateTime, Date, Boolean, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime as dt
from db.db import Base

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
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    office_license_id: Mapped[int | None] = mapped_column(ForeignKey("office_licenses.id", ondelete="SET NULL"), nullable=True, index=True)

    proprietaire: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    service: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    batiment: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)

    type_pc: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    marque: Mapped[str] = mapped_column(String(255), nullable=False, index=True)

    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ram: Mapped[str | None] = mapped_column(String(50), nullable=True)
    os: Mapped[str | None] = mapped_column(String(100), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(50), nullable=True)

    tag: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    nom_reseau: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    tag_chargeur: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True, unique=True)
    mac_ethernet: Mapped[str | None] = mapped_column(String(17), nullable=True, unique=True)
    mac_wifi: Mapped[str | None] = mapped_column(String(17), nullable=True, unique=True)

    clef_wifi: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    lecteur_cd: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    casque: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    absolute_dell: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    watt: Mapped[int | None] = mapped_column(Integer, nullable=True)

    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User | None] = relationship(back_populates="ordinateurs", passive_deletes=True)
    ecran: Mapped[list["Ecrans"]] = relationship(back_populates="ordinateur", passive_deletes=True)
    office_license: Mapped[OfficeLicenses | None] = relationship(back_populates="ordinateurs", passive_deletes=True)

class Ecrans(Base):
    __tablename__ = "ecrans"

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    taille: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    marque: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    modele: Mapped[str | None] = mapped_column(String(500), nullable=True, index=True)
    fournisseur: Mapped[str | None] = mapped_column(String(255), nullable=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fin_garantie: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateur_id: Mapped[int | None] = mapped_column(ForeignKey("ordinateurs.id", ondelete="SET NULL"), nullable=True, index=True)
    slot: Mapped[int | None] = mapped_column(Integer, nullable=True)

    ordinateur: Mapped[Optional["Ordinateurs"]] = relationship(back_populates="ecran")

    __table_args__ = (
        UniqueConstraint("ordinateur_id", "slot", name="uq_ecran_slot_per_pc"),
        CheckConstraint("slot IS NULL OR (slot BETWEEN 1 AND 5)", name="ck_slot_1_5"),
    )

class OfficeLicenses(Base):
    __tablename__ = "office_licenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    version: Mapped[str] = mapped_column(String(500), nullable=False, index=True)

    achat: Mapped[dt.date | None] = mapped_column(Date, nullable=True, index=True)
    numero_bc: Mapped[str | None] = mapped_column(String(255), nullable=True)
    type_license: Mapped[str | None] = mapped_column(String(50), nullable=True)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())

    ordinateurs: Mapped[list["Ordinateurs"]] = relationship(back_populates="office_license", passive_deletes=True)
