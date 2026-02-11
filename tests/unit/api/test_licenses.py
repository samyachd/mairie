import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.db import Base, get_db
from backend.db.models import OfficeLicenses

@pytest.fixture
def test_license(db_session):
    """
    Insère un écran de test dans la base.
    """
    license = OfficeLicenses(
        tag="OfficeLicense-TEST-001",
        proprietaire="Commune",
        version="Office License windows 2000"
    )

    db_session.add(license)
    db_session.commit()
    db_session.refresh(license)  # récupère l'id généré par la DB
    return license

def test_create_license(client):
    response = client.post("/licenses")
    assert response.status_code == 201
    assert response.json() == {
        "id": "12",
        "title": "Foo",
        "description": "vieux PC",
    }

def test_get_license(client, test_license):
    response = client.get(f"/licenses/{test_license.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_license.id
    assert data["tag"] == "OfficeLicense-TEST-001"