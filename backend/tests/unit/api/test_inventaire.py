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