import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.db import Base, get_db
from backend.db.models import Ordinateurs

@pytest.fixture
def test_ordinateur(db_session):
    """
    Insère un écran de test dans la base.
    """
    ordinateurs = Ordinateurs(
        tag="PC-TEST-001",
        proprietaire="Commune",
        service="Finances publiques",
        fournisseur="Atos",
        agent="Christine Lacomte",
        marque="Dell",
        nom_reseau="DESKTOP-TEST",
        numero_bc="056932302143434330594",
        fin_garantie="",
    )
    db_session.add(ordinateurs)
    db_session.commit()
    db_session.refresh(ordinateurs)  # récupère l'id généré par la DB
    return ordinateurs

def test_create_ordinateur(client):
    response = client.post("/ordinateurs", json={
        "tag": "PC-NEW-001",
        "marque": "Dell",
        "service": "Finances",
        "agent": "Jean Dupont",
    })
    assert response.status_code == 201
    
    data = response.json()
    assert data["tag"] == "PC-NEW-001"
    assert data["marque"] == "Dell"
    assert "id" in data

def test_get_ordinateurs(client, test_ordinateur):
    response = client.get(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_ordinateur.id
    assert data["tag"] == "PC-TEST-001"