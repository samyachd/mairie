import pytest
from db.models import OfficeLicenses

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

# -------- GET Methods (list all, list vide, lire, lire inexistant) -----------------

def test_get_license(client, test_license):
    response = client.get(f"/license/{test_license.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["proprietaire"] == "Commune"
    assert data["tag"] == "OfficeLicense-TEST-001"

def test_liste_license(client, test_license):
    response = client.get(f"/license")
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_liste_license_vide(client):
    response = client.get(f"/license")
    assert response.status_code == 200
    assert response.json() == []

def test_license_inexistant(client):
    response = client.get("/license/99999")
    assert response.status_code == 404

# -------- POST Methods -----------------

def test_create_license(client):
    response = client.post("/license", json={
        "tag": "OfficeLicense-TEST-002",
        "proprietaire": "Finances",
        "agent": "Jean Dupont",
        })
    assert response.status_code == 201

    data = response.json()
    assert data["tag"] == "OfficeLicense-TEST-002"
    assert data["proprietaire"] == "Finances"
    assert "id" in data

def test_creer_license_donnees_manquantes(client):
    response = client.post("/license", json={})
    assert response.status_code == 422

def test_creer_license_doublon(client, test_license):
    response = client.post(f"/license", json={
        "tag": "OfficeLicense-TEST-001",
        "proprietaire": "Commune",   
        })
    assert response.status_code == 409

# -------- PUT Methods ------------------------

def test_modifier_license(client, test_license):
    response = client.put(f"/license/{test_license.id}", json={
        "tag":"OfficeLicense-OLD-001",
        "proprietaire":"Mairie",
        "agent":"Jeanne"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["tag"] == "OfficeLicense-OLD-001"
    assert data["agent"] == "Jeanne"
    assert data["proprietaire"] == "Mairie"

def test_modifier_license_inexistant(client):
    response = client.put("/license/999999", json={
        "tag":"OfficeLicense-INEXISTANT-001"
    })
    assert response.status_code == 404

def test_modifier_license_donnees_invalides(client, test_license):
    response = client.put(f"/license/{test_license.id}", 
                content='{"tag": "OfficeLicense-001",}',
                headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422

# ----------- DELETE Methods ---------------------

def test_supprimer_license(client, test_license):
    response = client.delete(f"/license/{test_license.id}")
    assert response.status_code == 200

    response = client.get(f"/license/{test_license.id}")
    assert response.status_code == 404

def test_supprimer_license_inexistant(client):
    response = client.delete(f"/license/99999")
    assert response.status_code == 404

# ----------- AUTH Methods ------------------------

def test_creer_license_sans_auth(client_sans_auth):
    response = client_sans_auth.post("/license", json={
        "tag":"OfficeLicense-FAKE-001"
    })
    assert response.status_code == 401

def test_lire_license_sans_auth(client_sans_auth):
    response = client_sans_auth.get("/license")
    assert response.status_code == 401

def test_supprimer_license_sans_auth(client_sans_auth, test_license):
    response = client_sans_auth.delete(f"/license/{test_license.id}")
    assert response.status_code == 401

def test_modifier_license_sans_auth(client_sans_auth, test_license):
    response = client_sans_auth.put(f"/license/{test_license.id}")
    assert response.status_code == 401