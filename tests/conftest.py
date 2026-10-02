import pytest
from fastapi.testclient import TestClient
from src.api.main import app, get_pedido_repository
from src.repositories.memory_repository import InMemoryPedidoRepository

@pytest.fixture
def repo_memoria():
    repo = InMemoryPedidoRepository()
    yield repo
    repo.limpiar()

@pytest.fixture
def cliente_http(repo_memoria):
    app.dependency_overrides[get_pedido_repository] = lambda: repo_memoria
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
