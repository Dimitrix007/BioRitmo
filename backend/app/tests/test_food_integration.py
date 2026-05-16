# backend/app/tests/test_food_integration.py

"""
Testes de integração — Busca Nutricional via Open Food Facts API

Este módulo valida que:
1. O endpoint /api/v1/foods/search responde corretamente (com mock)
2. O serviço processa e filtra a resposta da API externa corretamente
3. A validação de parâmetros funciona (query obrigatória, mínimo 2 chars)
4. A API externa pode ser contactada diretamente (teste real — requer internet)
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

# ──────────────────────────────────────────────────────────────
# Dados mock que simulam uma resposta real da Open Food Facts
# ──────────────────────────────────────────────────────────────

MOCK_OFF_RESPONSE = {
    "products": [
        {
            "product_name": "Banana",
            "brands": "Dole",
            "nutriments": {
                "energy-kcal_100g": 89.0,
                "carbohydrates_100g": 22.8,
                "proteins_100g": 1.1,
                "fat_100g": 0.3,
            },
            "image_url": "https://example.com/banana.jpg",
        },
        {
            "product_name": "Banana Chips",
            "brands": "Generic",
            "nutriments": {
                "energy-kcal_100g": 519.0,
                "carbohydrates_100g": 58.0,
                "proteins_100g": 2.3,
                "fat_100g": 33.6,
            },
            "image_url": "",
        },
        {
            # Produto sem calorias — deve ser filtrado
            "product_name": "Produto Sem Calorias",
            "brands": "",
            "nutriments": {},
            "image_url": "",
        },
    ]
}

MOCK_EMPTY_RESPONSE = {"products": []}


# ──────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────

def make_mock_client(response_data: dict):
    """Cria um AsyncClient mockado que retorna response_data."""
    mock_response = MagicMock()
    mock_response.json.return_value = response_data
    mock_response.raise_for_status = MagicMock()

    mock_async_client = AsyncMock()
    mock_async_client.get = AsyncMock(return_value=mock_response)
    mock_async_client.__aenter__ = AsyncMock(return_value=mock_async_client)
    mock_async_client.__aexit__ = AsyncMock(return_value=None)

    return mock_async_client


# ──────────────────────────────────────────────────────────────
# Testes do Endpoint REST
# ──────────────────────────────────────────────────────────────

class TestFoodSearchEndpoint:
    """Testa o endpoint GET /api/v1/foods/search."""

    def test_search_retorna_resultados_validos(self):
        """O endpoint deve retornar resultados filtrados (sem produtos sem calorias)."""
        with patch("app.services.food_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value = make_mock_client(MOCK_OFF_RESPONSE)

            response = client.get("/api/v1/foods/search?q=banana")

        assert response.status_code == 200

        data = response.json()
        assert "results" in data
        assert "count" in data
        assert "query" in data
        assert data["query"] == "banana"
        assert data["count"] == 2  # 3 produtos, 1 sem calorias filtrado

    def test_search_estrutura_do_resultado(self):
        """Cada item retornado deve ter os campos nutricionais esperados."""
        with patch("app.services.food_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value = make_mock_client(MOCK_OFF_RESPONSE)

            response = client.get("/api/v1/foods/search?q=banana")

        data = response.json()
        required_fields = {
            "name", "brand", "calories_per_100g",
            "carbs_per_100g", "proteins_per_100g", "fats_per_100g",
        }
        for item in data["results"]:
            assert required_fields.issubset(item.keys()), (
                f"Item faltando campos: {required_fields - item.keys()}"
            )

    def test_search_valores_nutricionais_corretos(self):
        """Os valores nutricionais devem ser calculados corretamente."""
        with patch("app.services.food_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value = make_mock_client(MOCK_OFF_RESPONSE)

            response = client.get("/api/v1/foods/search?q=banana")

        data = response.json()
        banana = next(r for r in data["results"] if r["name"] == "Banana")

        assert banana["calories_per_100g"] == 89.0
        assert banana["carbs_per_100g"] == 22.8
        assert banana["proteins_per_100g"] == 1.1
        assert banana["fats_per_100g"] == 0.3

    def test_search_resultado_vazio(self):
        """Quando a API não retorna produtos, deve retornar lista vazia."""
        with patch("app.services.food_service.httpx.AsyncClient") as mock_cls:
            mock_cls.return_value = make_mock_client(MOCK_EMPTY_RESPONSE)

            response = client.get("/api/v1/foods/search?q=xyzabc123")

        assert response.status_code == 200
        data = response.json()
        assert data["results"] == []
        assert data["count"] == 0

    def test_search_sem_parametro_q_retorna_422(self):
        """A query 'q' é obrigatória — sem ela deve retornar 422."""
        response = client.get("/api/v1/foods/search")
        assert response.status_code == 422

    def test_search_query_muito_curta_retorna_422(self):
        """A query deve ter pelo menos 2 caracteres."""
        response = client.get("/api/v1/foods/search?q=a")
        assert response.status_code == 422

    def test_search_query_muito_longa_retorna_422(self):
        """A query não deve ter mais de 100 caracteres."""
        query_longa = "a" * 101
        response = client.get(f"/api/v1/foods/search?q={query_longa}")
        assert response.status_code == 422

    def test_search_erro_externo_retorna_503(self):
        """Quando a API externa falha, deve retornar 503."""
        with patch("app.services.food_service.httpx.AsyncClient") as mock_cls:
            mock_client = AsyncMock()
            mock_client.get = AsyncMock(side_effect=Exception("Timeout"))
            mock_client.__aenter__ = AsyncMock(return_value=mock_client)
            mock_client.__aexit__ = AsyncMock(return_value=None)
            mock_cls.return_value = mock_client

            response = client.get("/api/v1/foods/search?q=banana")

        assert response.status_code == 503


# ──────────────────────────────────────────────────────────────
# Teste de integração REAL (requer internet)
# Marcado com @pytest.mark.integration para separação
# ──────────────────────────────────────────────────────────────

@pytest.mark.integration
@pytest.mark.asyncio
async def test_integracao_real_open_food_facts():
    """
    Teste de integração real: contacta a Open Food Facts API.
    Requer conexão com a internet. Tolerante a falhas da API externa.
    """
    import httpx
    from app.services.food_service import search_foods

    try:
        results = await search_foods("apple", page_size=3)
        assert isinstance(results, list)
        if results:
            assert isinstance(results[0]["name"], str)
            assert results[0]["calories_per_100g"] > 0
    except httpx.HTTPStatusError as e:
        pytest.skip(f"API externa indisponível (HTTP {e.response.status_code}) — teste ignorado")
    except httpx.RequestError as e:
        pytest.skip(f"Sem conexão com a API externa — teste ignorado")