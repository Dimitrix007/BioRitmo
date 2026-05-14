"""Tests for exercise endpoints."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

NOW = datetime.now(UTC).isoformat()
VALID_EXERCISE = {
    "name": "Corrida",
    "description": "Corrida leve no parque",
    "calories_burned": 350.0,
    "duration_minutes": 30.0,
    "logged_at": NOW,
}


def test_create_exercise_valid():
    """Cenário válido: criar exercício com dados corretos."""
    response = client.post("/api/v1/exercises/", json=VALID_EXERCISE)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == VALID_EXERCISE["name"]
    assert data["calories_burned"] == VALID_EXERCISE["calories_burned"]
    assert "id" in data


def test_update_exercise_valid():
    """Cenário válido: atualizar exercício com novos dados."""
    create_resp = client.post("/api/v1/exercises/", json=VALID_EXERCISE)
    ex_id = create_resp.json()["id"]
    update = {"name": "Natação", "calories_burned": 500.0}
    response = client.put(f"/api/v1/exercises/{ex_id}", json=update)
    assert response.status_code == 200
    assert response.json()["name"] == "Natação"


def test_delete_exercise_valid():
    """Cenário válido: deletar exercício existente."""
    create_resp = client.post("/api/v1/exercises/", json=VALID_EXERCISE)
    ex_id = create_resp.json()["id"]
    assert client.delete(f"/api/v1/exercises/{ex_id}").status_code == 204
    assert client.get(f"/api/v1/exercises/{ex_id}").status_code == 404


def test_create_exercise_invalid_zero_duration():
    """Cenário inválido: duração zero deve ser rejeitada."""
    invalid = {**VALID_EXERCISE, "duration_minutes": 0.0}
    response = client.post("/api/v1/exercises/", json=invalid)
    assert response.status_code == 422


def test_create_exercise_invalid_missing_name():
    """Cenário inválido: nome ausente deve ser rejeitado."""
    invalid = {k: v for k, v in VALID_EXERCISE.items() if k != "name"}
    response = client.post("/api/v1/exercises/", json=invalid)
    assert response.status_code == 422


def test_get_exercise_not_found():
    """Cenário inválido: ID inexistente retorna 404."""
    response = client.get("/api/v1/exercises/99999")
    assert response.status_code == 404


def test_exercise_duration_boundary():
    """Caso limite: duração mínima positiva (0.1 min) é aceita."""
    exercise = {**VALID_EXERCISE, "duration_minutes": 0.1}
    response = client.post("/api/v1/exercises/", json=exercise)
    assert response.status_code == 201


def test_exercise_list_filtered_by_date():
    """Caso limite: filtro por data retorna lista (possivelmente vazia)."""
    response = client.get("/api/v1/exercises/?date=2000-01-01")
    assert response.status_code == 200
    assert response.json() == []
