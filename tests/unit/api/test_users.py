import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from backend.main import app
from backend.db.db import Base, get_db
from backend.db.models import User

@pytest.fixture
def test_users(db_session):
    """
    Insère un user de test dans la base.
    """
    user = User(
        name="achard",
        email="achard.samy@gmail.com",
        mot_de_passe_hash="fake_hash_pour_test",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # récupère l'id généré par la DB
    return user

def test_create_user(client):
    response = client.post("/users", json = {
        "name":"achord",
        "email":"achord.somy@gmail.com",
        "mot_de_passe_hash":"123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "achord"
    assert data["email"] == "achord.somy@gmail.com"
    assert "id" in data

def test_get_user(client, test_users):
    response = client.get(f"/users/{test_users.id}")
    data = response.json()
    assert data["name"] == "achard"
    assert data["email"] == "achard.samy@gmail.com"