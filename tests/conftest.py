import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models  # noqa: F401
from app.core.database import Base, get_db
from app.main import app as api


@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    Sessao = sessionmaker(bind=engine, autoflush=False)

    def override():
        db = Sessao()
        try:
            yield db
        finally:
            db.close()

    api.dependency_overrides[get_db] = override
    yield TestClient(api)
    api.dependency_overrides.clear()


def _auth(client, perfil, email):
    client.post("/usuarios", json={"nome": "Fulano", "email": email, "senha": "123456", "perfil": perfil})
    token = client.post("/login", json={"email": email, "senha": "123456"}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def prof(client):
    return _auth(client, "professor", "prof@teste.com")


@pytest.fixture
def aluno(client):
    return _auth(client, "aluno", "aluno@teste.com")


@pytest.fixture
def atividade_payload():
    return {
        "titulo": "Valor de f(3)",
        "enunciado": "Dada f(x) = 2x + 1, calcule f(3).",
        "nivel": 1,
        "representacao": "algebrica",
        "tipo_pergunta": "valor_em_x",
        "coef_a": 2,
        "coef_b": 1,
        "x_dado": 3,
    }
