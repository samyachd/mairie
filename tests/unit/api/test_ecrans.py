import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.db import Base, get_db
from backend.db.models import Ecrans

@pytest.fixture
def test_ecran(db_session):
    """
    Insère un écran de test dans la base.
    """
    ecran = Ecrans(
        tag="ecran-TEST-001",
        proprietaire="Privé",
        service="Finances",
        fournisseur="Atos",
        agent="Christine Lacomte",
        marque="Dell",
        nom_reseau="DESKTOP-TEST",
        numero_bc="056932302143434330594",
        fin_garantie="",
    )
    db_session.add(ecran)
    db_session.commit()
    db_session.refresh(ecran)  # récupère l'id généré par la DB
    return ecran

def test_create_ecran(client):
    response = client.post("/ecrans", json={
        "tag": "ecran-NEW-001",
        "marque": "Dell",
        "service": "Finances",
        "agent": "Jean Dupont",
        })
    assert response.status_code == 201

    data = response.json()
    assert data["tag"] == "ecran-NEW-001"
    assert data["marque"] == "Dell"
    assert "id" in data
    
def test_get_ecran(client, test_ecran):
    response = client.get(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["fournisseur"] == "Atos"
    assert data["tag"] == "ecran-TEST-001"

def test_liste_ecrans(client, test_ecran):
    response = client.get(f"/ecrans")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_liste_ecran_vide(client):
    response = client.get(f"/ecrans")
    assert response.status_code == 200
    assert response.json() == []

def test_ecran_inexistant(client):
    response = client.get("/ecrans/99999")
    assert response.status_code == 404

def test_creer_ecran_donnees_invalides(client):
    response = client.post("/ecrans", json={})
    assert response.status_code == 200

def test_supprimer_ecran(client, test_ecran):
    response = client.delete(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 200

    response = client.get(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 404
