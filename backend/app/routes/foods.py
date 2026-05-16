# backend/app/routes/foods.py

from fastapi import APIRouter, HTTPException, Query
from app.services.food_service import search_foods

router = APIRouter(prefix="/api/v1/foods", tags=["foods"])


@router.get("/search", summary="Buscar alimentos por nome")
async def search_food_items(
    q: str = Query(
        ...,
        min_length=2,
        max_length=100,
        description="Nome do alimento a buscar (mínimo 2 caracteres)",
        example="banana",
    )
):
    """
    Busca alimentos na base Open Food Facts e retorna informações nutricionais.

    - **q**: Nome do alimento (ex: banana, arroz integral, peito de frango)

    Retorna lista com nome, calorias por 100g, macronutrientes e imagem.
    """
    try:
        results = await search_foods(q)
        return {
            "query": q,
            "results": results,
            "count": len(results),
            "source": "Open Food Facts (https://world.openfoodfacts.org)",
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Serviço de busca de alimentos temporariamente indisponível: {str(e)}",
        )