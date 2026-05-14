/**
 * meals.js — Meals CRUD page
 */

import { MealAPI }                                      from './api.js';
import { toast, confirm, openModal, closeModal,
         setLoading, setEmpty, formatDate,
         nowLocalISO, btnLoading }                       from './ui.js';

let editingId = null;

export function initMeals() {
  document.getElementById('btn-add-meal').addEventListener('click', () => openAddModal());
  document.getElementById('meal-form').addEventListener('submit', handleSubmit);
  document.getElementById('meal-filter-date').addEventListener('change', loadMeals);
  document.getElementById('btn-clear-meal-filter').addEventListener('click', () => {
    document.getElementById('meal-filter-date').value = '';
    loadMeals();
  });
  loadMeals();
}

async function loadMeals() {
  const tbody    = document.getElementById('meals-tbody');
  const dateVal  = document.getElementById('meal-filter-date').value;
  setLoading(tbody, 'Carregando refeições...');
  try {
    const meals = await MealAPI.list(dateVal);
    renderTable(meals);
  } catch (e) {
    toast('Erro ao carregar refeições: ' + e.message, 'error');
    setEmpty(tbody, 'Erro ao carregar dados.');
  }
}

function renderTable(meals) {
  const tbody = document.getElementById('meals-tbody');
  if (!meals.length) { setEmpty(tbody, 'Nenhuma refeição registrada.'); return; }

  tbody.innerHTML = meals.map(m => `
    <tr>
      <td><strong>${esc(m.name)}</strong><br><small style="color:var(--text-muted)">${esc(m.description || '')}</small></td>
      <td><span class="badge badge-yellow">🔥 ${m.calories} kcal</span></td>
      <td><span class="badge badge-blue">💧 ${m.water_ml} ml</span></td>
      <td style="color:var(--text-secondary);font-size:.8rem">${formatDate(m.logged_at)}</td>
      <td>
        <div style="display:flex;gap:6px">
          <button class="btn btn-ghost btn-sm btn-icon" onclick="window._editMeal(${m.id})" title="Editar">✏️</button>
          <button class="btn btn-danger btn-sm btn-icon" onclick="window._deleteMeal(${m.id},'${esc(m.name)}')" title="Deletar">🗑️</button>
        </div>
      </td>
    </tr>`).join('');
}

function openAddModal() {
  editingId = null;
  document.getElementById('meal-modal-title').textContent = 'Nova Refeição';
  document.getElementById('meal-form').reset();
  document.getElementById('meal-logged-at').value = nowLocalISO();
  openModal('meal-modal-overlay');
}

window._editMeal = async (id) => {
  try {
    const m = await MealAPI.get(id);
    editingId = id;
    document.getElementById('meal-modal-title').textContent = 'Editar Refeição';
    document.getElementById('meal-name').value        = m.name;
    document.getElementById('meal-desc').value        = m.description || '';
    document.getElementById('meal-calories').value    = m.calories;
    document.getElementById('meal-water').value       = m.water_ml;
    document.getElementById('meal-logged-at').value   = m.logged_at.slice(0, 16);
    openModal('meal-modal-overlay');
  } catch (e) {
    toast('Erro ao carregar refeição: ' + e.message, 'error');
  }
};

window._deleteMeal = async (id, name) => {
  const ok = await confirm(`Deseja deletar a refeição "${name}"?`);
  if (!ok) return;
  try {
    await MealAPI.delete(id);
    toast('Refeição deletada!', 'success');
    loadMeals();
  } catch (e) {
    toast('Erro ao deletar: ' + e.message, 'error');
  }
};

async function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('meal-submit-btn');
  btnLoading(btn, true);

  const payload = {
    name:        document.getElementById('meal-name').value.trim(),
    description: document.getElementById('meal-desc').value.trim() || null,
    calories:    parseFloat(document.getElementById('meal-calories').value),
    water_ml:    parseFloat(document.getElementById('meal-water').value) || 0,
    logged_at:   document.getElementById('meal-logged-at').value,
  };

  try {
    if (editingId) {
      await MealAPI.update(editingId, payload);
      toast('Refeição atualizada!', 'success');
    } else {
      await MealAPI.create(payload);
      toast('Refeição registrada!', 'success');
    }
    closeModal('meal-modal-overlay');
    loadMeals();
  } catch (e) {
    toast('Erro: ' + e.message, 'error');
  } finally {
    btnLoading(btn, false);
  }
}

function esc(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
