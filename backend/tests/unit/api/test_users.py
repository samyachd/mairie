import pytest
from backend.db.models import User

@pytest.fixture
def test_user(db_session):
    """
    Insère un user de test dans la base.
    """
    user = User(
        name="test-001",
        email="test.test@gmail.com",
        mot_de_passe_hash="fake_hash_pour_test",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # récupère l'id généré par la DB
    return user

# -------- GET Methods (list all, list vide, lire, lire inexistant) -----------------

def test_get_user(client, test_user):
    response = client.get(f"/users/{test_user.id}")
    data = response.json()
    assert data["name"] == "test-001"
    assert data["email"] == "test.test@gmail.com"

def test_liste_user(client, test_user):
    response = client.get(f"/users")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_liste_user_vide(client):
    response = client.get(f"/users")
    assert response.status_code == 200
    assert response.json() == []

def test_user_inexistant(client):
    response = client.get("/users/99999")
    assert response.status_code == 404

# -------- POST Methods -----------------

def test_create_user(client):
    response = client.post("/users", json = {
        "name":"test2",
        "email":"test2.test@gmail.com",
        "mot_de_passe_hash":"123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "test2"
    assert data["email"] == "test2.test@gmail.com"
    assert "id" in data


def test_creer_user_donnees_manquantes(client):
    response = client.post("/users", json={})
    assert response.status_code == 422

def test_creer_user_doublon(client, test_user):
    response = client.post(f"/users", json={
        "name": "test",
        "email": "test.test@gmail.com",   
        })
    assert response.status_code == 409

def test_create_user_pas_de_mot_de_passe_en_reponse(client):
    response = client.post("/users", json={
        "name": "test2",
        "email": "test2.test@gmail.com",
        "mot_de_passe": "123456"
    })
    data = response.json()
    assert "mot_de_passe" not in data
    assert "mot_de_passe_hash" not in data

# -------- PUT Methods ------------------------

def test_modifier_user(client, test_user):
    response = client.put(f"/users/{test_user.id}", json={
        "name":"test3",
        "email":"test3@gmail.com",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test3"
    assert data["email"] == "test3@gmail.com"

def test_modifier_user_inexistant(client):
    response = client.put("/users/999999", json={
        "name":"test4"
    })
    assert response.status_code == 404

def test_modifier_user_donnees_invalides(client, test_user):
    response = client.put(f"/users/{test_user.id}", 
                content='{"name": "test1",}',
                headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422

# ----------- DELETE Methods ---------------------

def test_supprimer_user(client, test_user):
    response = client.delete(f"/users/{test_user.id}")
    assert response.status_code == 200

    response = client.get(f"/users/{test_user.id}")
    assert response.status_code == 404

def test_supprimer_user_inexistant(client):
    response = client.delete(f"/users/99999")
    assert response.status_code == 404

# ----------- AUTH Methods ------------------------

def test_creer_user_sans_auth(client_sans_auth):
    response = client_sans_auth.post("/users", json={
        "name":"test1"
    })
    assert response.status_code == 401

def test_lire_user_sans_auth(client_sans_auth):
    response = client_sans_auth.get("/users")
    assert response.status_code == 401

def test_supprimer_user_sans_auth(client_sans_auth, test_user):
    response = client_sans_auth.delete(f"/users/{test_user.id}")
    assert response.status_code == 401

def test_modifier_user_sans_auth(client_sans_auth, test_user):
    response = client_sans_auth.put(f"/users/{test_user.id}")
    assert response.status_code == 401