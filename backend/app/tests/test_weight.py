"""Tests for weight log endpoints."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

NOW = datetime.now(UTC).isoformat()
VALID_LOG = {
    "weight_kg": 75.5,
    "logged_at": NOW,
}


def test_create_weight_log_valid():
    """Cenário válido: registrar peso com dados corretos."""
    response = client.post("/api/v1/weight/", json=VALID_LOG)
    assert response.status_code == 201
    data = response.json()
    assert data["weight_kg"] == VALID_LOG["weight_kg"]
    assert "id" in data


def test_list_weight_logs():
    """Cenário válido: listar logs retorna lista."""
    client.post("/api/v1/weight/", json=VALID_LOG)
    response = client.get("/api/v1/weight/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_update_weight_log_valid():
    """Cenário válido: atualizar peso existente."""
    create_resp = client.post("/api/v1/weight/", json=VALID_LOG)
    log_id = create_resp.json()["id"]
    response = client.put(f"/api/v1/weight/{log_id}", json={"weight_kg": 74.0})
    assert response.status_code == 200
    assert response.json()["weight_kg"] == 74.0


def test_create_weight_log_invalid_negative():
    """Cenário inválido: peso negativo deve ser rejeitado."""
    invalid = {**VALID_LOG, "weight_kg": -10.0}
    response = client.post("/api/v1/weight/", json=invalid)
    assert response.status_code == 422


def test_create_weight_log_boundary_high():
    """Caso limite: peso >= 500 kg deve ser rejeitado."""
    invalid = {**VALID_LOG, "weight_kg": 500.0}
    response = client.post("/api/v1/weight/", json=invalid)
    assert response.status_code == 422


def test_delete_weight_log_not_found():
    """Cenário inválido: deletar ID inexistente retorna 404."""
    response = client.delete("/api/v1/weight/99999")
    assert response.status_code == 404


def test_delete_weight_log_valid():
    """Cenário válido: deletar registro existente."""
    create_resp = client.post("/api/v1/weight/", json=VALID_LOG)
    log_id = create_resp.json()["id"]
    assert client.delete(f"/api/v1/weight/{log_id}").status_code == 204
    assert client.get(f"/api/v1/weight/{log_id}").status_code == 404


def test_weight_boundary_minimum():
    """Caso limite: peso muito baixo mas válido (0.1 kg) é aceito."""
    log = {**VALID_LOG, "weight_kg": 0.1}
    response = client.post("/api/v1/weight/", json=log)
    assert response.status_code == 201
