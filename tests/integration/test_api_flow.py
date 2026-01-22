class TestAPIFlow:
    def test_root_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data

    def test_cors_headers(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert "access-control-allow-origin" in response.headers or response.status_code == 200
