import pytest
from backend.app.db.models import User


class TestUsersRouter:
    
    def test_get_users_empty(self, client, db_session):
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_user(self, client, db_session):
        user_data = {"name": "John Doe", "email": "john@example.com"}
        response = client.post("/users/", json=user_data)
        assert response.status_code in [200, 201]
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
    
    def test_get_user_by_id(self, client, db_session):
        user = User(name="Jane Doe", email="jane@example.com")
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        response = client.get(f"/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        
        response = client.get(f"/users/{user.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
