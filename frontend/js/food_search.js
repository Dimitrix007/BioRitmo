import { searchFoods } from "./api.js";

/**
 * Executa a busca de alimentos e renderiza os resultados
 */
export async function searchFoodNutrition() {
  const input = document.getElementById("food-search-input");
  const resultsContainer = document.getElementById("food-search-results");

  const query = input.value.trim();

  if (query.length < 2) {
    showFoodMessage(resultsContainer, "⚠️ Digite pelo menos 2 caracteres.", "warning");
    return;
  }

  // Estado de loading
  resultsContainer.classList.remove("hidden");
  resultsContainer.innerHTML = `
    <div class="food-loading">
      <span class="food-spinner"></span> Buscando informações nutricionais...
    </div>`;

  try {
    const foods = await searchFoods(query);

    if (foods.length === 0) {
      showFoodMessage(
        resultsContainer,
        `😕 Nenhum alimento encontrado para "<strong>${query}</strong>". Tente outro nome.`,
        "empty"
      );
      return;
    }

    renderFoodResults(resultsContainer, foods);
  } catch (error) {
    showFoodMessage(
      resultsContainer,
      `❌ Erro ao buscar: ${error.message}`,
      "error"
    );
  }
}

/**
 * Renderiza os cards de resultado de alimento
 */
function renderFoodResults(container, foods) {
  const cards = foods.map((food) => createFoodCard(food)).join("");
  container.innerHTML = `
    <p class="food-results-label">
      📦 Selecione um alimento para preencher as calorias automaticamente:
    </p>
    <div class="food-cards-grid">${cards}</div>
  `;
}

/**
 * Cria o HTML de um card de alimento
 */
function createFoodCard(food) {
  const brand = food.brand ? `<span class="food-brand">${food.brand}</span>` : "";
  const img = food.image_url
    ? `<img src="${food.image_url}" alt="${food.name}" class="food-img" onerror="this.style.display='none'" />`
    : `<div class="food-img-placeholder">🍽️</div>`;

  return `
    <button
      type="button"
      class="food-card"
      onclick='selectFood(${JSON.stringify(food)})'
      title="Clique para usar ${food.name}"
    >
      ${img}
      <div class="food-card-info">
        <p class="food-name">${food.name}</p>
        ${brand}
        <div class="food-macros">
          <span class="macro kcal">🔥 ${food.calories_per_100g} kcal</span>
          <span class="macro prot">💪 ${food.proteins_per_100g}g prot</span>
          <span class="macro carb">🌾 ${food.carbs_per_100g}g carb</span>
          <span class="macro fat">🥑 ${food.fats_per_100g}g gord</span>
        </div>
        <p class="food-per100">por 100g</p>
      </div>
    </button>`;
}

/**
 * Preenche o formulário com os dados do alimento selecionado
 * Ajuste os IDs conforme os inputs do seu formulário de refeição
 */
export function selectFood(food) {
  // Preenche o nome da refeição (se o campo estiver vazio)
  const nameInput = document.getElementById("meal-name");
  if (nameInput && !nameInput.value) {
    nameInput.value = food.name;
  }

  // Preenche as calorias com base em 100g
  const caloriesInput = document.getElementById("meal-calories");
  if (caloriesInput) {
    caloriesInput.value = food.calories_per_100g;
  }

  // Fecha os resultados e limpa o campo de busca
  const resultsContainer = document.getElementById("food-search-results");
  if (resultsContainer) {
    resultsContainer.classList.add("hidden");
    resultsContainer.innerHTML = "";
  }

  const searchInput = document.getElementById("food-search-input");
  if (searchInput) {
    searchInput.value = "";
  }

  // Feedback visual
  if (caloriesInput) {
    caloriesInput.classList.add("field-filled");
    setTimeout(() => caloriesInput.classList.remove("field-filled"), 1500);
  }

  // Toast de confirmação (adapte ao sistema de toast do seu projeto)
  if (typeof showToast === "function") {
    showToast(`✅ "${food.name}" selecionado — ${food.calories_per_100g} kcal/100g`, "success");
  }
}

/**
 * Exibe mensagem de estado (vazio, erro, aviso)
 */
function showFoodMessage(container, html, type) {
  container.classList.remove("hidden");
  container.innerHTML = `<p class="food-message food-message--${type}">${html}</p>`;
}

// Expõe as funções para o escopo global (necessário para onclick inline)
window.searchFoodNutrition = searchFoodNutrition;
window.selectFood = selectFood;