/**
 * api.js — Centralized API client for BioRitmo
 * All fetch calls go through here.
 */

const BASE_URL = 'http://localhost:8000/api/v1';

async function request(method, path, body = null) {
  const opts = {
    method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (body) opts.body = JSON.stringify(body);

  const res = await fetch(`${BASE_URL}${path}`, opts);

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
  list:   (date = '') => request('GET', `/meals/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/meals/${id}`),
  create: (body)      => request('POST', '/meals/', body),
  update: (id, body)  => request('PUT', `/meals/${id}`, body),
  delete: (id)        => request('DELETE', `/meals/${id}`),
};

// ─── Exercises ────────────────────────────────────────────────
export const ExerciseAPI = {
  list:   (date = '') => request('GET', `/exercises/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/exercises/${id}`),
  create: (body)      => request('POST', '/exercises/', body),
  update: (id, body)  => request('PUT', `/exercises/${id}`, body),
  delete: (id)        => request('DELETE', `/exercises/${id}`),
};

// ─── Weight ───────────────────────────────────────────────────
export const WeightAPI = {
  list:   (date = '') => request('GET', `/weight/${date ? `?date=${date}` : ''}`),
  get:    (id)        => request('GET', `/weight/${id}`),
  create: (body)      => request('POST', '/weight/', body),
  update: (id, body)  => request('PUT', `/weight/${id}`, body),
  delete: (id)        => request('DELETE', `/weight/${id}`),
};

// ─── Dashboard ────────────────────────────────────────────────
export const DashboardAPI = {
  summary: (date = '') => request('GET', `/dashboard/summary${date ? `?target_date=${date}` : ''}`),
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