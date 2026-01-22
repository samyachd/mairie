class TestEcransRouter:
    def test_get_ecrans_empty(self, client, db_session):
        response = client.get("/ecrans/")
        assert response.status_code == 200
        assert response.json() == []
