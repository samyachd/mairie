"""
Script de seed pour initialiser la base de données.
Idempotent : peut être relancé sans créer de doublons.

Usage :
    docker compose exec backend uv run python -m utils.seed
"""
import datetime as dt
from sqlalchemy.orm import Session

from core.security import hacher_mot_de_passe
from db.session import SessionLocal
from db.models.user import User, RoleEnum
from db.models.agent import Agent
from db.models.ordinateur import Ordinateur
from db.models.ecran import Ecran
from db.models.office_licence import OfficeLicence


# ─────────────────────────────────────────────────────────────
# Configuration du seed
# ─────────────────────────────────────────────────────────────

ADMIN_EMAIL = "admin@mairie.fr"
ADMIN_PASSWORD = "Admin1234!"

USER_EMAIL = "user@mairie.fr"
USER_PASSWORD = "User1234!"

READER_EMAIL = "reader@mairie.fr"
READER_PASSWORD = "Reader1234!"


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def get_or_create_user(db: Session, email: str, password: str, nom: str, role: RoleEnum) -> User:
    """Crée un user s'il n'existe pas déjà. Retourne le user (créé ou existant)."""
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"  → {email} existe déjà, skip")
        return existing
    
    user = User(
        email=email,
        nom=nom,
        mot_de_passe_hash=hacher_mot_de_passe(password),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"  ✓ {email} créé ({role.value})")
    return user


def get_or_create_agent(db: Session, nom: str, prenom: str, service: str, email: str) -> Agent:
    """Crée un agent s'il n'existe pas déjà."""
    existing = db.query(Agent).filter(Agent.email == email).first()
    if existing:
        print(f"  → {prenom} {nom} existe déjà, skip")
        return existing
    
    agent = Agent(
        nom=nom,
        prenom=prenom,
        service=service,
        email=email,
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    print(f"  ✓ {prenom} {nom} ({service})")
    return agent


# ─────────────────────────────────────────────────────────────
# Étapes du seed
# ─────────────────────────────────────────────────────────────

def seed_users(db: Session) -> None:
    print("\n👤 Users")
    get_or_create_user(db, ADMIN_EMAIL, ADMIN_PASSWORD, "Admin Principal", RoleEnum.admin)
    get_or_create_user(db, USER_EMAIL, USER_PASSWORD, "Utilisateur Standard", RoleEnum.user)
    get_or_create_user(db, READER_EMAIL, READER_PASSWORD, "Lecteur Seul", RoleEnum.read)


def seed_agents(db: Session) -> list[Agent]:
    print("\n👔 Agents")
    agents_data = [
        ("Dupont", "Jean", "Service Technique", "jean.dupont@mairie.fr"),
        ("Martin", "Marie", "Ressources Humaines", "marie.martin@mairie.fr"),
        ("Durand", "Sophie", "Finances", "sophie.durand@mairie.fr"),
        ("Bernard", "Pierre", "Urbanisme", "pierre.bernard@mairie.fr"),
        ("Petit", "Claire", "État Civil", "claire.petit@mairie.fr"),
    ]
    agents = [
        get_or_create_agent(db, nom, prenom, service, email)
        for nom, prenom, service, email in agents_data
    ]
    return agents


def seed_ordinateurs(db: Session, agents: list[Agent]) -> list[Ordinateur]:
    """Crée 5 ordinateurs fictifs, chacun assigné à un agent."""
    print("\n💻 Ordinateurs")
    
    # Si des ordis existent déjà, on skip tout le bloc
    if db.query(Ordinateur).count() > 0:
        print("  → Des ordinateurs existent déjà, skip")
        return db.query(Ordinateur).all()
    
    ordis_data = [
        # (tag, marque, modele_ram, os, nom_reseau, date_achat)
        ("ORD-001", "Dell", "16 Go", "Windows 11", "PC-DUPONT", dt.date(2023, 3, 15)),
        ("ORD-002", "HP", "8 Go", "Windows 11", "PC-MARTIN", dt.date(2024, 1, 20)),
        ("ORD-003", "Lenovo", "32 Go", "Windows 11", "PC-DURAND", dt.date(2024, 6, 10)),
        ("ORD-004", "Dell", "16 Go", "Windows 10", "PC-BERNARD", dt.date(2022, 9, 5)),
        ("ORD-005", "HP", "16 Go", "Windows 11", "PC-PETIT", dt.date(2025, 2, 28)),
    ]
    
    ordis = []
    for i, (tag, marque, ram, os, nom_reseau, date_achat) in enumerate(ordis_data):
        ordi = Ordinateur(
            tag=tag,
            marque=marque,
            ram=ram,
            os=os,
            nom_reseau=nom_reseau,
            date_achat=date_achat,
            type_equipement="Portable" if i % 2 == 0 else "Fixe",
            service=agents[i].service,
            proprietaire=f"{agents[i].prenom} {agents[i].nom}",
            batiment="Mairie Principale" if i < 3 else "Annexe",
            fournisseur="Infotel",
        )
        db.add(ordi)
        db.flush()  # pour récupérer l'ID
        
        # Assigne l'ordi à l'agent (FK côté Agent)
        ordi.agent_id = agents[i].id
        
        ordis.append(ordi)
        print(f"  ✓ {tag} - {marque} {ram} ({agents[i].prenom} {agents[i].nom})")
    
    db.commit()
    return ordis


def seed_ecrans(db: Session, ordis: list[Ordinateur]) -> None:
    """Crée des écrans : 1 pour les 2 premiers ordis, 2 pour les autres."""
    print("\n🖥️  Écrans")
    
    if db.query(Ecran).count() > 0:
        print("  → Des écrans existent déjà, skip")
        return
    
    ecrans_data = [
        # (tag, marque, taille, ordi_index, slot)
        ("ECR-001", "Dell", "24\"", 0, 1),
        ("ECR-002", "HP", "22\"", 1, 1),
        ("ECR-003", "LG", "27\"", 2, 1),
        ("ECR-004", "LG", "27\"", 2, 2),   # 2e écran pour PC-DURAND
        ("ECR-005", "Dell", "24\"", 3, 1),
        ("ECR-006", "Samsung", "27\"", 4, 1),
        ("ECR-007", "Samsung", "24\"", 4, 2),  # 2e écran pour PC-PETIT
    ]
    
    for tag, marque, taille, ordi_index, slot in ecrans_data:
        ordi = ordis[ordi_index]
        ecran = Ecran(
            tag=tag,
            marque=marque,
            taille=taille,
            slot=slot,
            ordinateur_id=ordi.id,
            date_achat=ordi.date_achat,  # même date que l'ordi
            type_equipement="Écran",
            service=ordi.service,
            batiment=ordi.batiment,
            fournisseur="Infotel",
        )
        db.add(ecran)
        print(f"  ✓ {tag} - {marque} {taille} (slot {slot} sur {ordi.tag})")
    
    db.commit()


def seed_licences(db: Session) -> None:
    print("\n📀 Licences Office")
    
    if db.query(OfficeLicence).count() > 0:
        print("  → Des licences existent déjà, skip")
        return
    
    licences_data = [
        ("Microsoft 365 Business Standard", "2024", dt.date(2024, 1, 1), "Microsoft Direct"),
        ("Microsoft 365 E3", "2024", dt.date(2024, 1, 1), "Microsoft Direct"),
        ("Office 2021 Standard", "2021", dt.date(2022, 6, 15), "Bechtle"),
    ]
    
    for type_lic, version, date_achat, fournisseur in licences_data:
        licence = OfficeLicence(
            type_licence=type_lic,
            version=version,
            date_achat=date_achat,
            fournisseur=fournisseur,
        )
        db.add(licence)
        print(f"  ✓ {type_lic} ({version})")
    
    db.commit()


# ─────────────────────────────────────────────────────────────
# Point d'entrée
# ─────────────────────────────────────────────────────────────

def main() -> None:
    print("🌱 Seeding database...")
    db = SessionLocal()
    try:
        seed_users(db)
        agents = seed_agents(db)
        ordis = seed_ordinateurs(db, agents)
        seed_ecrans(db, ordis)
        seed_licences(db)
        print("\n✅ Seed terminé avec succès\n")
    except Exception as e:
        print(f"\n❌ Erreur pendant le seed : {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()