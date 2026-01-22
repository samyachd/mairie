import pytest


class TestOrdinateursRouter:
    
    def test_get_ordinateurs_empty(self, client, db_session):
        response = client.get("/ordinateurs/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_ordinateur(self, client, db_session):
        ordinateur_data = {
            "type_pc": "Desktop",
            "marque": "Dell",
            "proprietaire": "John Doe",
            "service": "IT"
        }
        response = client.post("/ordinateurs/", json=ordinateur_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["type_pc"] == "Desktop"
        assert data["marque"] == "Dell"
