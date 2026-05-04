"""
Normalize the wide-format inventory JSON in data/clean_extracts/ into the
shape expected by the SQLAlchemy models in db/models/ (Ordinateur, Ecran,
OfficeLicence).

Reads the most recent seed_data_*.json from data/clean_extracts/ and writes
data/clean_extracts/normalized_<timestamp>.json with three top-level keys:
    - ordinateurs : list[dict]
    - ecrans      : list[dict]   (linked to ordinateurs via _ordinateur_tag)
    - office_licences : list[dict] (referenced by ordinateurs._office_key)

Usage (from backend/):
    uv run python -m utils.clean_to_models
"""
from __future__ import annotations

import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

INPUT_DIR = Path(__file__).resolve().parents[2] / "data" / "clean_extracts"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT = INPUT_DIR / f"normalized_{TIMESTAMP}.json"

PLACEHOLDER_NULLS = {"", "?????????", "????", "N/A", "NA", "-", "—"}

PC_FIXE_KEYWORDS = ("FIXE", "OPTIPLEX", "MICRO PC", "AIO", "ECOLES", "TOUT EN UN")
PC_PORT_KEYWORDS = ("PORTABLE", "LATITUDE", "PRECISION", "SURFACE", "TABLETTE", "XPS")
ECRAN_KEYWORDS = ("ECRAN",)


# ──────────────────────────────────────────────────────────────────────────
# Value coercion helpers
# ──────────────────────────────────────────────────────────────────────────

def clean_str(v) -> str | None:
    if v is None:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    if s in PLACEHOLDER_NULLS:
        return None
    return s or None


def to_bool(v) -> bool | None:
    """Boolean fields contain free text in source: 'OUI', 'OUI PRÊT 12/03/2024',
    'X', 'INTEGRE', 'NON', etc. Anything non-empty/non-negative reads as True."""
    s = clean_str(v)
    if s is None:
        return None
    low = s.lower()
    if low in {"non", "no", "false", "0", "n"}:
        return False
    return True


def to_date(v) -> str | None:
    """Source dates look like '2020-12-14 00:00:00'. Return ISO 'YYYY-MM-DD'."""
    s = clean_str(v)
    if s is None:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y", "%d/%m/%Y %H:%M:%S"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    return None  # silently drop unparseable dates


def to_mac(v) -> str | None:
    s = clean_str(v)
    if s is None:
        return None
    s = s.lower().replace("-", ":")
    if not re.fullmatch(r"[0-9a-f:]{11,23}", s):
        return None
    return s


def to_ip(v) -> str | None:
    s = clean_str(v)
    if s is None:
        return None
    if not re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", s):
        return None
    return s


# ──────────────────────────────────────────────────────────────────────────
# Bucketing
# ──────────────────────────────────────────────────────────────────────────

def bucket_type(raw: str | None) -> str | None:
    """Map the 25 raw TYPE values to a small set used by the UI."""
    s = clean_str(raw)
    if s is None:
        return None
    upper = s.upper()
    if any(k in upper for k in ECRAN_KEYWORDS) and "PORTABLE" not in upper:
        return "ECRAN"
    if any(k in upper for k in PC_PORT_KEYWORDS):
        return "PC PORTABLE"
    if any(k in upper for k in PC_FIXE_KEYWORDS):
        return "PC FIXE"
    return s  # keep original if unknown


# ──────────────────────────────────────────────────────────────────────────
# Row → model dicts
# ──────────────────────────────────────────────────────────────────────────

ECRAN_SLOTS = [
    # (slot, type_key, marque_key, modele_key, serie_key, fournisseur_key, achat_key, garantie_key)
    (1, "TYPE ECRAN 1", "MARQUE ECRAN 1", "MODELE ECRAN 1", "N° SERIE ECRAN 1",
     "FOURNISSEUR ECRAN 1", "DATE ACHAT ECRAN 1", "DATE FIN GARANTIE ECRAN 1"),
    (2, "TYPE ECRAN 2", "MARQUE ECRAN 2", "MODELE ECRAN 2", "N° SERIE ECRAN 2",
     "FOURNISSEUR ECRAN 2", "DATE ACHAT ECRAN 2", "DATE FIN GARANTIE ECRAN 2"),
    (3, "TYPE ECRAN 3", "MARQUE ECRAN 3", "MODELE ECRAN 3", "N° SERIE ECRAN 3",
     "FOURNISSEUR ECRAN 3", "DATE ACHAT ECRAN 3", "DATE FIN GARANTIE ECRAN 3"),
    (4, "TYPE ECRAN TELETRAVAIL", "MARQUE ECRAN TELETRAVAIL", "MODELE ECRAN TELETRAVAIL",
     "N° SERIE ECRAN TELETRAVAIL", "FOURNISSEUR ECRAN TELETRAVAIL",
     "DATE ACHAT ECRAN TELETRAVAIL", "DATE FIN GARANTIE ECRAN TELETRAVAIL"),
    # Excel collision: pandas auto-suffixed the 5th teletravail group
    (5, "TYPE ECRAN TELETRAVAIL2", "MARQUE ECRAN TELETRAVAIL3", "MODELE ECRAN TELETRAVAIL4",
     "N° SERIE ECRAN TELETRAVAIL5", "FOURNISSEUR ECRAN TELETRAVAIL6",
     "DATE ACHAT ECRAN TELETRAVAIL8", "DATE FIN GARANTIE ECRAN TELETRAVAIL2"),
]


def build_ordinateur(row: dict) -> dict | None:
    tag = clean_str(row.get("N° SERIE PC"))
    date_achat = to_date(row.get("DATE ACHAT PC"))
    type_eq = bucket_type(row.get("TYPE"))

    # Skip rows that aren't a PC: no serial AND not labelled as a PC type
    if tag is None and type_eq not in {"PC FIXE", "PC PORTABLE"}:
        return None
    # Model requires date_achat NOT NULL
    if date_achat is None:
        return None

    return {
        "tag": tag,
        "type_equipement": type_eq,
        "service": clean_str(row.get("SERVICE")),
        "batiment": clean_str(row.get("EMPLACEMENT")),
        "proprietaire": clean_str(row.get("UTILISATEUR PRINCIPAL")),
        "marque": clean_str(row.get("MARQUE PC")),
        "fournisseur": clean_str(row.get("FOURNISSEUR PC")),
        "date_achat": date_achat,
        "fin_garantie": to_date(row.get("DATE FIN GARANTIE PC")),
        "ram": clean_str(row.get("RAM PC")),
        "os": clean_str(row.get("OS")),
        "nom_reseau": clean_str(row.get("NOM RESEAU")),
        "ip_address": to_ip(row.get("Adresse IP PC")),
        "mac_ethernet": to_mac(row.get("MAC ADRESSE ETHERNET")),
        "mac_wifi": to_mac(row.get("MAC ADRESSE WIFI")),
        "clef_wifi": to_bool(row.get("CLEF WIFI")),
        "lecteur_cd": to_bool(row.get("LECTEUR DVD/CD EXTERNE")),
        "casque": to_bool(row.get("CASQUE")),
        "absolute_dell": to_bool(row.get("ABSOLUTE DELL")),
    }


def build_ecrans(row: dict, ordi_tag: str | None) -> list[dict]:
    ecrans = []
    service = clean_str(row.get("SERVICE"))
    batiment = clean_str(row.get("EMPLACEMENT"))
    for slot, k_type, k_marque, k_modele, k_serie, k_four, k_achat, k_garantie in ECRAN_SLOTS:
        type_e = clean_str(row.get(k_type))
        marque = clean_str(row.get(k_marque))
        modele = clean_str(row.get(k_modele))
        serie = clean_str(row.get(k_serie))
        date_achat = to_date(row.get(k_achat))
        # Slot is empty if nothing identifies it
        if not any([type_e, marque, modele, serie, date_achat]):
            continue
        # Model requires date_achat NOT NULL
        if date_achat is None:
            continue
        ecrans.append({
            "tag": serie,
            "slot": slot,
            "taille": type_e,                    # values like 'LCD 22"' fit BaseEquipement.taille semantics
            "marque": " ".join(filter(None, [marque, modele])) or None,
            "type_equipement": "ECRAN",
            "service": service,
            "batiment": batiment,
            "fournisseur": clean_str(row.get(k_four)),
            "date_achat": date_achat,
            "fin_garantie": to_date(row.get(k_garantie)),
            "_ordinateur_tag": ordi_tag,         # link key, resolved at seed time
        })
    return ecrans


def build_office_licence(row: dict) -> dict | None:
    """OfficeLicence requires version + date_achat NOT NULL."""
    version = clean_str(row.get("VERSION OFFICE"))
    date_achat = to_date(row.get("DATE ACHAT OFFICE"))
    if version is None or date_achat is None:
        return None
    return {
        "type_licence": clean_str(row.get("TYPE LICENCE OFFICE")),
        "version": version,
        "date_achat": date_achat,
        "fournisseur": clean_str(row.get("FOURNISSEUR OFFICE")),
    }


def office_dedupe_key(lic: dict) -> tuple:
    return (lic["version"], lic["date_achat"], lic.get("type_licence"), lic.get("fournisseur"))


# ──────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────

def main() -> None:
    files = sorted(INPUT_DIR.glob("seed_data_*.json"))
    if not files:
        raise SystemExit(f"No seed_data_*.json found in {INPUT_DIR}")
    src = files[-1]
    print(f"Reading {src.name}")

    rows = json.loads(src.read_text(encoding="utf-8"))

    ordinateurs: list[dict] = []
    ecrans: list[dict] = []
    licences: dict[tuple, dict] = {}
    seen_pc_tags: set[str] = set()
    skipped = Counter()

    for row in rows:
        ordi = build_ordinateur(row)

        if ordi is not None:
            # Drop duplicate PCs by tag (some serials repeat across rows)
            if ordi["tag"] and ordi["tag"] in seen_pc_tags:
                skipped["duplicate_pc_tag"] += 1
                ordi = None
            else:
                if ordi["tag"]:
                    seen_pc_tags.add(ordi["tag"])

                lic = build_office_licence(row)
                if lic is not None:
                    key = office_dedupe_key(lic)
                    if key not in licences:
                        licences[key] = lic
                    ordi["_office_key"] = list(key)
                else:
                    ordi["_office_key"] = None

                ordinateurs.append(ordi)
        else:
            if clean_str(row.get("N° SERIE PC")) and not to_date(row.get("DATE ACHAT PC")):
                skipped["pc_no_date_achat"] += 1
            elif clean_str(row.get("TYPE")) and "ECRAN" not in str(row.get("TYPE")).upper():
                skipped["row_not_a_pc"] += 1

        ordi_tag = ordi["tag"] if ordi else None
        ecrans.extend(build_ecrans(row, ordi_tag))

    output = {
        "ordinateurs": ordinateurs,
        "ecrans": ecrans,
        "office_licences": list(licences.values()),
    }

    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Wrote {OUTPUT.name}")
    print(f"  ordinateurs    : {len(ordinateurs)}")
    print(f"    with office  : {sum(1 for o in ordinateurs if o.get('_office_key'))}")
    print(f"    with tag     : {sum(1 for o in ordinateurs if o.get('tag'))}")
    print(f"  ecrans         : {len(ecrans)}")
    print(f"    linked to PC : {sum(1 for e in ecrans if e.get('_ordinateur_tag'))}")
    print(f"  office_licences: {len(licences)}")
    if skipped:
        print(f"  skipped        : {dict(skipped)}")


if __name__ == "__main__":
    main()
