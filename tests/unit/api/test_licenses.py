import pytest


class TestLicensesRouter:
    
    def test_get_licenses_empty(self, client, db_session):
        response = client.get("/licenses/")
        assert response.status_code == 200
        assert response.json() == []
