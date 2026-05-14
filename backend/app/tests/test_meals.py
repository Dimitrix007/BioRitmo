"""Tests for meal endpoints — valid, invalid, and boundary scenarios."""

from datetime import UTC, datetime

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

NOW = datetime.now(UTC).isoformat()
VALID_MEAL = {
    "name": "Almoço saudável",
    "description": "Arroz, feijão e frango grelhado",
    "calories": 600.0,
    "water_ml": 300.0,
    "logged_at": NOW,
}


# ─── Cenário Válido ───────────────────────────────────────────────────────────

def test_create_meal_valid():
    """Cenário válido: criar uma refeição com dados corretos."""
    response = client.post("/api/v1/meals/", json=VALID_MEAL)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == VALID_MEAL["name"]
    assert data["calories"] == VALID_MEAL["calories"]
    assert data["water_ml"] == VALID_MEAL["water_ml"]
    assert "id" in data


def test_list_meals_valid():
    """Cenário válido: listar refeições retorna lista."""
    client.post("/api/v1/meals/", json=VALID_MEAL)
    response = client.get("/api/v1/meals/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_meal_by_id_valid():
    """Cenário válido: buscar refeição por ID existente."""
    create_resp = client.post("/api/v1/meals/", json=VALID_MEAL)
    meal_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/meals/{meal_id}")
    assert response.status_code == 200
    assert response.json()["id"] == meal_id


def test_update_meal_valid():
    """Cenário válido: atualizar refeição com dados corretos."""
    create_resp = client.post("/api/v1/meals/", json=VALID_MEAL)
    meal_id = create_resp.json()["id"]
    update = {"name": "Jantar light", "calories": 400.0}
    response = client.put(f"/api/v1/meals/{meal_id}", json=update)
    assert response.status_code == 200
    assert response.json()["name"] == "Jantar light"
    assert response.json()["calories"] == 400.0


def test_delete_meal_valid():
    """Cenário válido: deletar refeição existente."""
    create_resp = client.post("/api/v1/meals/", json=VALID_MEAL)
    meal_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/meals/{meal_id}")
    assert response.status_code == 204
    get_resp = client.get(f"/api/v1/meals/{meal_id}")
    assert get_resp.status_code == 404


# ─── Cenário Inválido ─────────────────────────────────────────────────────────

def test_create_meal_invalid_negative_calories():
    """Cenário inválido: calorias negativas devem ser rejeitadas."""
    invalid = {**VALID_MEAL, "calories": -100.0}
    response = client.post("/api/v1/meals/", json=invalid)
    assert response.status_code == 422


def test_create_meal_invalid_missing_name():
    """Cenário inválido: nome ausente deve ser rejeitado."""
    invalid = {k: v for k, v in VALID_MEAL.items() if k != "name"}
    response = client.post("/api/v1/meals/", json=invalid)
    assert response.status_code == 422


def test_get_meal_not_found():
    """Cenário inválido: ID inexistente retorna 404."""
    response = client.get("/api/v1/meals/99999")
    assert response.status_code == 404


def test_delete_meal_not_found():
    """Cenário inválido: deletar ID inexistente retorna 404."""
    response = client.delete("/api/v1/meals/99999")
    assert response.status_code == 404


# ─── Caso Limite ──────────────────────────────────────────────────────────────

def test_create_meal_zero_water():
    """Caso limite: água = 0 é permitido."""
    meal = {**VALID_MEAL, "water_ml": 0.0}
    response = client.post("/api/v1/meals/", json=meal)
    assert response.status_code == 201
    assert response.json()["water_ml"] == 0.0


def test_create_meal_very_high_calories():
    """Caso limite: calorias muito altas (mas positivas) são aceitas."""
    meal = {**VALID_MEAL, "calories": 9999.0}
    response = client.post("/api/v1/meals/", json=meal)
    assert response.status_code == 201
    assert response.json()["calories"] == 9999.0


def test_create_meal_name_too_long():
    """Caso limite: nome com mais de 100 caracteres é rejeitado."""
    meal = {**VALID_MEAL, "name": "A" * 101}
    response = client.post("/api/v1/meals/", json=meal)
    assert response.status_code == 422
