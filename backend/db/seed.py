import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db.session import get_db
from db.models.user import User
from db.models import Ordinateur, Ecran, OfficeLicence, Agent
from core.security import hacher_mot_de_passe

def seed():
    db = next(get_db())
    data_path = Path(__file__).parent / "data" / "seed_data.json"
    
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    # Config — modèle + champ unique pour éviter les doublons
    mappings = [
        ("ordinateurs", Ordinateur, "numero_serie"),
        ("ecrans", Ecran, "numero_serie"),
        ("licences", OfficeLicence, "numero_serie"),
        ("agents", Agent, "email"),
    ]

    for cle, Modele, champ_unique in mappings:
        items = data.get(cle, [])
        created = 0
        for item in items:
            valeur_unique = item.get(champ_unique)
            existe = db.query(Modele).filter(
                getattr(Modele, champ_unique) == valeur_unique
            ).first()
            if not existe:
                db.add(Modele(**item))
                created += 1
        db.flush()
        print(f"✅ {cle} : {created}/{len(items)} créés")

    # Admin par défaut
    if not db.query(User).filter(User.username == "admin").first():
        db.add(User(
            username="admin",
            email="admin@mairie.fr",
            hashed_password=hacher_mot_de_passe("admin123"),
            role="admin",
            is_active=True
        ))
        print("Admin créé : admin / admin123")

    db.commit()
    print("\nSeed terminé !")

if __name__ == "__main__":
    seed()



