# backend/app/services/food_service.py

import httpx
from typing import List, Dict, Any

OPENFOODFACTS_URL = "https://world.openfoodfacts.org/cgi/search.pl"

FIELDS = "product_name,nutriments,brands,image_url,categories_tags"


async def search_foods(query: str, page_size: int = 6) -> List[Dict[str, Any]]:
    """
    Busca alimentos na Open Food Facts API pelo nome.

    Args:
        query: Nome do alimento a buscar (ex: "banana", "arroz")
        page_size: Número máximo de resultados (padrão: 6)

    Returns:
        Lista de dicionários com informações nutricionais dos alimentos
    """
    params = {
        "search_terms": query,
        "action": "process",
        "json": "true",
        "page_size": page_size,
        "fields": FIELDS,
        "sort_by": "popularity_key",
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get(OPENFOODFACTS_URL, params=params)
        response.raise_for_status()
        data = response.json()

    products = []

    for product in data.get("products", []):
        name = product.get("product_name", "").strip()
        if not name:
            continue

        nutriments = product.get("nutriments", {})

        # Tenta diferentes chaves para calorias
        calories = (
            nutriments.get("energy-kcal_100g")
            or nutriments.get("energy-kcal")
            or 0
        )

        # Filtra produtos sem informação calórica
        if not calories or float(calories) <= 0:
            continue

        products.append(
            {
                "name": name,
                "brand": product.get("brands", "").split(",")[0].strip(),
                "calories_per_100g": round(float(calories), 1),
                "carbs_per_100g": round(
                    float(nutriments.get("carbohydrates_100g", 0)), 1
                ),
                "proteins_per_100g": round(
                    float(nutriments.get("proteins_100g", 0)), 1
                ),
                "fats_per_100g": round(float(nutriments.get("fat_100g", 0)), 1),
                "image_url": product.get("image_url", ""),
            }
        )

    return products