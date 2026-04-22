import pytest
from jose import jwt
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta, timezone
from db.db import Base
from db.session import get_db
from main import app
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

JWT_KEY = os.environ.get("JWT_KEY")
ALGORITHM = "HS256"

@pytest.fixture
def fake_token():
    payload = {
        "sub": "user_test@mairie.fr",
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }
    if not JWT_KEY:
        raise ValueError("JWT_KEY non définie ! Vérifie ton fichier .env")
    else:
        token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
        return token

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        client.headers["Authorization"] = f"Bearer {fake_token}"
        yield client

    app.dependency_overrides.clear()

@pytest.fixture
def client_sans_auth(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c  # Pas de token !

    app.dependency_overrides.clear()