import pytest
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

# -------- GET Methods (list all, list vide, lire, lire inexistant) -----------------

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

# -------- POST Methods -----------------

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

def test_creer_ecran_donnees_manquantes(client):
    response = client.post("/ecrans", json={})
    assert response.status_code == 422

def test_creer_ecran_doublon(client, test_ecran):
    response = client.post(f"/ecrans/", json={
        "tag": "ecran-TEST-001",
        "marque": "Dell",
        "service": "Finances",
        "agent": "Christine Lacomte"   
        })
    assert response.status_code == 409

# -------- PUT Methods ------------------------

def test_modifier_ecran(client, test_ecran):
    response = client.put(f"/ecrans/{test_ecran.id}", json={
        "tag":"ecran-OLD-001",
        "marque":"IBM",
        "service":"Informatique",
        "agent":"Marie"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["tag"] == "ecran-OLD-001"
    assert data["agent"] == "Marie"
    assert data["marque"] == "IBM"
    assert data["service"] == "Informatique"

def test_modifier_ecran_inexistant(client):
    response = client.put("/ecrans/999999", json={
        "tag":"ecran-INEXISTANT-001"
    })
    assert response.status_code == 404

def test_modifier_ecran_donnees_invalides(client, test_ecran):
    response = client.put(f"/ecrans/{test_ecran.id}", 
                content='{"tag": "ecran-001",}',
                headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422

# ----------- DELETE Methods ---------------------

def test_supprimer_ecran(client, test_ecran):
    response = client.delete(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 200

    response = client.get(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 404

def test_supprimer_ecran_inexistant(client):
    response = client.delete(f"/ecrans/99999")
    assert response.status_code == 404

# ----------- AUTH Methods ------------------------

def test_creer_ecran_sans_auth(client_sans_auth):
    response = client_sans_auth.post("/ecrans", json={
        "tag":"new-ECRAN-999",
        "proprietaire":"test"
    })
    assert response.status_code == 401

def test_lire_ecrans_sans_auth(client_sans_auth, test_ecran):
    response = client_sans_auth.get("/ecrans")
    assert response.status_code == 401

def test_supprimer_ecrans_sans_auth(client_sans_auth, test_ecran):
    response = client_sans_auth.delete(f"/ecrans/{test_ecran.id}")
    assert response.status_code == 401

def test_modifier_ecrans_sans_auth(client_sans_auth, test_ecran):
    response = client_sans_auth.put(f"/ecrans/{test_ecran.id}", json={
        "tag":"new-ECRAN-999",
        "proprietaire":"test"
    })
    assert response.status_code == 401


