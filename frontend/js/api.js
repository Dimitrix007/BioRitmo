/**
 * api.js — Centralized API client for BioRitmo
 * All fetch calls go through here.
 */

const API_BASE = window.location.hostname === "localhost" ||
                 window.location.hostname === "127.0.0.1"
  ? "http://127.0.0.1:8000"
  : "https://bioritmo-api.onrender.com";
  
async function request(method, path, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${API_BASE}${path}`, opts);

  if (res.status === 204) return null;

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const msg = data?.detail || `Erro ${res.status}`;
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data;
}

// ─── Meals ────────────────────────────────────────────────────
export const MealAPI = {
  list:   (date = '') => request('GET', `/api/v1/meals/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/api/v1/meals/${id}`),
  create: (body)      => request('POST', '/api/v1/meals/', body),
  update: (id, body)  => request('PUT', `/api/v1/meals/${id}`, body),
  delete: (id)        => request('DELETE', `/api/v1/meals/${id}`),
};

// ─── Exercises ────────────────────────────────────────────────
export const ExerciseAPI = {
  list:   (date = '') => request('GET', `/api/v1/exercises/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/api/v1/exercises/${id}`),
  create: (body)      => request('POST', '/api/v1/exercises/', body),
  update: (id, body)  => request('PUT', `/api/v1/exercises/${id}`, body),
  delete: (id)        => request('DELETE', `/api/v1/exercises/${id}`),
};

// ─── Weight ───────────────────────────────────────────────────
export const WeightAPI = {
  list:   (date = '') => request('GET', `/api/v1/weight/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/api/v1/weight/${id}`),
  create: (body)      => request('POST', '/api/v1/weight/', body),
  update: (id, body)  => request('PUT', `/api/v1/weight/${id}`, body),
  delete: (id)        => request('DELETE', `/api/v1/weight/${id}`),
};

// ─── Dashboard ────────────────────────────────────────────────
export const DashboardAPI = {
  summary: (date = '') => request('GET', `/api/v1/dashboard/summary${date ? `?target_date=${date}` : ''}`),
};

// ─── Busca nutricional via Open Food Facts (intermediada pelo backend) ───────

/**
 * Busca alimentos pelo nome na Open Food Facts via backend BioRitmo.
 * @param {string} query - Nome do alimento a buscar
 * @returns {Promise<Array>} - Lista de alimentos com dados nutricionais
 */
export async function searchFoods(query) {
  const encodedQuery = encodeURIComponent(query.trim());
  const response = await fetch(`${API_BASE}/api/v1/foods/search?q=${encodedQuery}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Erro ao buscar alimentos");
  }

  const data = await response.json();
  return data.results;
}