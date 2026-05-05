"""Seed the inventory DB from data/clean_extracts/normalized_*.json
(produced by utils.clean_to_models).

Idempotent: re-running skips rows already present (matched by tag for
equipment, by (version, date_achat, type_licence, fournisseur) for licences).

Usage (from backend/):
    docker compose exec backend uv run python -m db.seed
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.session import SessionLocal
from db.models import Agent, Ecran, Ordinateur, OfficeLicence
from db.models.user import User, RoleEnum
from core.security import hacher_mot_de_passe


CLEAN_DIR = Path(__file__).resolve().parents[2] / "data" / "clean_extracts"

ADMIN_EMAIL = "admin@mairie.fr"
ADMIN_PASSWORD = "Admin1234!"


# ──────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────

def _parse_date(s: str | None) -> dt.date | None:
    return dt.date.fromisoformat(s) if s else None


def _latest_normalized_file() -> Path:
    files = sorted(CLEAN_DIR.glob("normalized_*.json"))
    if not files:
        raise SystemExit(
            f"No normalized_*.json found in {CLEAN_DIR}. "
            "Run `uv run python -m utils.clean_to_models` first."
        )
    return files[-1]


# ──────────────────────────────────────────────────────────────────────
# Seed steps
# ──────────────────────────────────────────────────────────────────────

def seed_admin(db) -> None:
    if db.query(User).filter(User.email == ADMIN_EMAIL).first():
        print(f"  → admin already exists ({ADMIN_EMAIL})")
        return
    db.add(
        User(
            nom="Admin",
            email=ADMIN_EMAIL,
            mot_de_passe_hash=hacher_mot_de_passe(ADMIN_PASSWORD),
            role=RoleEnum.admin,
        )
    )
    db.commit()
    print(f"  ✓ admin created ({ADMIN_EMAIL} / {ADMIN_PASSWORD})")


def seed_office_licences(db, items: list[dict]) -> dict[tuple, OfficeLicence]:
    """Insert licences and return a map { (version, date_achat, type_licence,
    fournisseur) → OfficeLicence } so ordinateurs can resolve their _office_key."""
    by_key: dict[tuple, OfficeLicence] = {}
    created = 0
    for raw in items:
        key = (
            raw.get("version"),
            raw.get("date_achat"),
            raw.get("type_licence"),
            raw.get("fournisseur"),
        )
        existing = (
            db.query(OfficeLicence)
            .filter(
                OfficeLicence.version == key[0],
                OfficeLicence.date_achat == _parse_date(key[1]),
                OfficeLicence.type_licence == key[2],
                OfficeLicence.fournisseur == key[3],
            )
            .first()
        )
        if existing:
            by_key[key] = existing
            continue
        lic = OfficeLicence(
            version=raw.get("version"),
            type_licence=raw.get("type_licence"),
            date_achat=_parse_date(raw.get("date_achat")),
            fournisseur=raw.get("fournisseur"),
        )
        db.add(lic)
        db.flush()
        by_key[key] = lic
        created += 1
    print(f"  ✓ office_licences : {created}/{len(items)} created")
    return by_key


def seed_ordinateurs(
    db, items: list[dict], licences_by_key: dict[tuple, OfficeLicence]
) -> dict[str, Ordinateur]:
    """Insert ordinateurs. Returns { tag → Ordinateur } so écrans can link."""
    by_tag: dict[str, Ordinateur] = {}
    created = 0
    skipped_dup = 0
    for raw in items:
        tag = raw.get("tag")
        if tag:
            existing = (
                db.query(Ordinateur).filter(Ordinateur.tag == tag).first()
            )
            if existing:
                by_tag[tag] = existing
                skipped_dup += 1
                continue

        office_key = raw.get("_office_key")
        office_id = (
            licences_by_key[tuple(office_key)].id
            if office_key and tuple(office_key) in licences_by_key
            else None
        )

        ordi = Ordinateur(
            tag=tag,
            type_equipement=raw.get("type_equipement"),
            service=raw.get("service"),
            batiment=raw.get("batiment"),
            proprietaire=raw.get("proprietaire"),
            marque=raw.get("marque"),
            fournisseur=raw.get("fournisseur"),
            date_achat=_parse_date(raw.get("date_achat")),
            fin_garantie=_parse_date(raw.get("fin_garantie")),
            ram=raw.get("ram"),
            os=raw.get("os"),
            nom_reseau=raw.get("nom_reseau"),
            ip_address=raw.get("ip_address"),
            mac_ethernet=raw.get("mac_ethernet"),
            mac_wifi=raw.get("mac_wifi"),
            clef_wifi=raw.get("clef_wifi"),
            lecteur_cd=raw.get("lecteur_cd"),
            casque=raw.get("casque"),
            absolute_dell=raw.get("absolute_dell"),
            office_licence_id=office_id,
        )
        db.add(ordi)
        db.flush()
        if tag:
            by_tag[tag] = ordi
        created += 1
    print(
        f"  ✓ ordinateurs    : {created}/{len(items)} created"
        f" (skipped {skipped_dup} duplicates by tag)"
    )
    return by_tag


def seed_ecrans(
    db, items: list[dict], ordis_by_tag: dict[str, Ordinateur]
) -> None:
    created = 0
    skipped_dup = 0
    skipped_slot = 0
    for raw in items:
        tag = raw.get("tag")
        if tag:
            existing = db.query(Ecran).filter(Ecran.tag == tag).first()
            if existing:
                skipped_dup += 1
                continue

        owner_tag = raw.get("_ordinateur_tag")
        ordi = ordis_by_tag.get(owner_tag) if owner_tag else None
        ordi_id = ordi.id if ordi else None
        slot = raw.get("slot") if ordi_id is not None else None

        # Slot is unique per ordinateur; skip if already taken
        if ordi_id is not None and slot is not None:
            taken = (
                db.query(Ecran)
                .filter(Ecran.ordinateur_id == ordi_id, Ecran.slot == slot)
                .first()
            )
            if taken:
                skipped_slot += 1
                continue

        ecran = Ecran(
            tag=tag,
            slot=slot,
            taille=raw.get("taille"),
            marque=raw.get("marque"),
            type_equipement=raw.get("type_equipement"),
            service=raw.get("service"),
            batiment=raw.get("batiment"),
            fournisseur=raw.get("fournisseur"),
            date_achat=_parse_date(raw.get("date_achat")),
            fin_garantie=_parse_date(raw.get("fin_garantie")),
            ordinateur_id=ordi_id,
        )
        db.add(ecran)
        created += 1
    db.flush()
    print(
        f"  ✓ ecrans         : {created}/{len(items)} created"
        f" (skipped {skipped_dup} duplicates by tag, {skipped_slot} slot conflicts)"
    )


# ──────────────────────────────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────────────────────────────

def seed() -> None:
    src = _latest_normalized_file()
    print(f"Reading {src}")
    data = json.loads(src.read_text(encoding="utf-8"))

    db = SessionLocal()
    try:
        print("\n👤 Admin")
        seed_admin(db)

        print("\n📀 Office licences")
        licences_by_key = seed_office_licences(db, data.get("office_licences", []))

        print("\n💻 Ordinateurs")
        ordis_by_tag = seed_ordinateurs(db, data.get("ordinateurs", []), licences_by_key)

        print("\n🖥️  Écrans")
        seed_ecrans(db, data.get("ecrans", []), ordis_by_tag)

        db.commit()
        print("\n✅ Seed terminé")
    except Exception as e:
        db.rollback()
        print(f"\n❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
