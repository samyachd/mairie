import os
from datetime import datetime, timedelta, timezone
from typing import Generator

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from core.settings import settings
from db.db import Base
from db.models.user import User
from db.session import get_db
from main import app

# Charge le .env si présent (local). En CI, les env vars sont fournies par GitHub Actions.
load_dotenv()


# ─────────────────────────────────────────────────────────────
# Engine & DB
# ─────────────────────────────────────────────────────────────

def get_test_database_url() -> str:
    """
    Construit l'URL de la DB de test.
    - En CI (variables DB_HOST etc. fournies) → Postgres
    - En local (pas de variables ou flag explicite) → SQLite in-memory
    """
    if os.getenv("USE_POSTGRES_TESTS") == "true" or os.getenv("CI") == "true":
        user = os.environ["DB_USER"]
        password = os.environ["DB_PASS"]
        host = os.environ["DB_HOST"]
        port = os.environ.get("DB_PORT", "5432")
        name = os.environ["DB_NAME"]
        return f"postgresql://{user}:{password}@{host}:{port}/{name}"
    return "sqlite:///:memory:"


@pytest.fixture(scope="session")
def db_engine():
    """Engine SQLAlchemy partagé pour toute la session pytest."""
    url = get_test_database_url()
    
    if url.startswith("sqlite"):
        engine = create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = create_engine(url)
    
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    """
    Session isolée : chaque test tourne dans une transaction
    rollback à la fin → aucune fuite entre tests.
    """
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


# ─────────────────────────────────────────────────────────────
# Utilisateurs de test (créés en DB pour que get_current_user marche)
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def test_admin_user(db_session: Session) -> User:
    """Crée un utilisateur admin en DB pour le test courant."""
    user = User(
        email="admin_test@mairie.fr",
        hashed_password="fake_hash_not_used_in_tests",
        role="admin",
        # Ajoute ici les autres champs obligatoires de ton modèle User
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_user(db_session: Session) -> User:
    """Crée un utilisateur standard en DB pour le test courant."""
    user = User(
        email="user_test@mairie.fr",
        hashed_password="fake_hash_not_used_in_tests",
        role="user",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# ─────────────────────────────────────────────────────────────
# Tokens JWT
# ─────────────────────────────────────────────────────────────

def _make_token(email: str) -> str:
    """Génère un JWT valide pour un email donné, en utilisant les settings réels."""
    payload = {
        "sub": email,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


@pytest.fixture
def admin_token(test_admin_user: User) -> str:
    return _make_token(test_admin_user.email)


@pytest.fixture
def user_token(test_user_user: User) -> str:
    return _make_token(test_user_user.email)


# ─────────────────────────────────────────────────────────────
# Clients HTTP
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Client sans authentification."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def admin_client(db_session: Session, admin_token: str) -> Generator[TestClient, None, None]:
    """Client authentifié comme admin."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers["Authorization"] = f"Bearer {admin_token}"
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def user_client(db_session: Session, user_token: str) -> Generator[TestClient, None, None]:
    """Client authentifié comme user standard."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        c.headers["Authorization"] = f"Bearer {user_token}"
        yield c
    app.dependency_overrides.clear()