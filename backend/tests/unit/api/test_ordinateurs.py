import pytest
from backend.db.models.models import Ordinateurs

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

# -------- GET Methods (list all, list vide, lire, lire inexistant) -----------------

def test_get_ordinateur(client, test_ordinateur):
    response = client.get(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["proprietaire"] == "Commune"
    assert data["tag"] == "PC-TEST-001"

def test_liste_ordinateur(client, test_ordinateur):
    response = client.get(f"/ordinateurs")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_liste_ordinateur_vide(client):
    response = client.get(f"/ordinateurs")
    assert response.status_code == 200
    assert response.json() == []

def test_ordinateur_inexistant(client):
    response = client.get("/ordinateurs/99999")
    assert response.status_code == 404

# -------- POST Methods -----------------

def test_create_ordinateur(client):
    response = client.post("/ordinateurs", json={
        "tag": "PC-TEST-002",
        "proprietaire": "Finances",
        "agent": "Jean Dupont",
        })
    assert response.status_code == 201

    data = response.json()
    assert data["tag"] == "PC-TEST-002"
    assert data["proprietaire"] == "Finances"
    assert "id" in data

def test_creer_ordinateurs_donnees_manquantes(client):
    response = client.post("/ordinateurs", json={})
    assert response.status_code == 422

def test_creer_ordinateurs_doublon(client, test_ordinateur):
    response = client.post(f"/ordinateurs", json={
        "tag": "PC-TEST-001",
        "proprietaire": "Commune",   
        })
    assert response.status_code == 409

# -------- PUT Methods ------------------------

def test_modifier_ordinateur(client, test_ordinateur):
    response = client.put(f"/ordinateurs/{test_ordinateur.id}", json={
        "tag":"PC-OLD-001",
        "proprietaire":"Mairie",
        "agent":"Jeanne"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["tag"] == "PC-OLD-001"
    assert data["agent"] == "Jeanne"
    assert data["proprietaire"] == "Mairie"

def test_modifier_ordinateur_inexistant(client):
    response = client.put("/ordinateurs/999999", json={
        "tag":"PC-INEXISTANT-001"
    })
    assert response.status_code == 404

def test_modifier_ordinateur_donnees_invalides(client, test_ordinateur):
    response = client.put(f"/ordinateurs/{test_ordinateur.id}", 
                content='{"tag": "PC-001",}',
                headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422

# ----------- DELETE Methods ---------------------

def test_supprimer_ordinateur(client, test_ordinateur):
    response = client.delete(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 200

    response = client.get(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 404

def test_supprimer_ordinateur_inexistant(client):
    response = client.delete(f"/ordinateurs/99999")
    assert response.status_code == 404

# ----------- AUTH Methods ------------------------

def test_creer_ordinateur_sans_auth(client_sans_auth):
    response = client_sans_auth.post("/ordinateurs", json={
        "tag":"PC-FAKE-001"
    })
    assert response.status_code == 401

def test_lire_ordinateur_sans_auth(client_sans_auth):
    response = client_sans_auth.get("/ordinateurs")
    assert response.status_code == 401

def test_supprimer_ordinateur_sans_auth(client_sans_auth, test_ordinateur):
    response = client_sans_auth.delete(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 401

def test_modifier_ordinateur_sans_auth(client_sans_auth, test_ordinateur):
    response = client_sans_auth.put(f"/ordinateurs/{test_ordinateur.id}")
    assert response.status_code == 401