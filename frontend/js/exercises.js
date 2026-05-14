/**
 * exercises.js — Exercises CRUD page
 */

import { ExerciseAPI }                                   from './api.js';
import { toast, confirm, openModal, closeModal,
         setLoading, setEmpty, formatDate,
         nowLocalISO, btnLoading }                        from './ui.js';

let editingId = null;

export function initExercises() {
  document.getElementById('btn-add-exercise').addEventListener('click', () => openAddModal());
  document.getElementById('exercise-form').addEventListener('submit', handleSubmit);
  document.getElementById('exercise-filter-date').addEventListener('change', loadExercises);
  document.getElementById('btn-clear-exercise-filter').addEventListener('click', () => {
    document.getElementById('exercise-filter-date').value = '';
    loadExercises();
  });
  loadExercises();
}

async function loadExercises() {
  const tbody   = document.getElementById('exercises-tbody');
  const dateVal = document.getElementById('exercise-filter-date').value;
  setLoading(tbody, 'Carregando exercícios...');
  try {
    const exercises = await ExerciseAPI.list(dateVal);
    renderTable(exercises);
  } catch (e) {
    toast('Erro ao carregar exercícios: ' + e.message, 'error');
    setEmpty(tbody, 'Erro ao carregar dados.');
  }
}

function renderTable(exercises) {
  const tbody = document.getElementById('exercises-tbody');
  if (!exercises.length) { setEmpty(tbody, 'Nenhum exercício registrado.'); return; }

  tbody.innerHTML = exercises.map(ex => `
    <tr>
      <td><strong>${esc(ex.name)}</strong><br><small style="color:var(--text-muted)">${esc(ex.description || '')}</small></td>
      <td><span class="badge badge-red">🔥 ${ex.calories_burned} kcal</span></td>
      <td><span class="badge badge-purple">⏱️ ${ex.duration_minutes} min</span></td>
      <td style="color:var(--text-secondary);font-size:.8rem">${formatDate(ex.logged_at)}</td>
      <td>
        <div style="display:flex;gap:6px">
          <button class="btn btn-ghost btn-sm btn-icon" onclick="window._editExercise(${ex.id})" title="Editar">✏️</button>
          <button class="btn btn-danger btn-sm btn-icon" onclick="window._deleteExercise(${ex.id},'${esc(ex.name)}')" title="Deletar">🗑️</button>
        </div>
      </td>
    </tr>`).join('');
}

function openAddModal() {
  editingId = null;
  document.getElementById('exercise-modal-title').textContent = 'Novo Exercício';
  document.getElementById('exercise-form').reset();
  document.getElementById('exercise-logged-at').value = nowLocalISO();
  openModal('exercise-modal-overlay');
}

window._editExercise = async (id) => {
  try {
    const ex = await ExerciseAPI.get(id);
    editingId = id;
    document.getElementById('exercise-modal-title').textContent = 'Editar Exercício';
    document.getElementById('exercise-name').value        = ex.name;
    document.getElementById('exercise-desc').value        = ex.description || '';
    document.getElementById('exercise-calories').value    = ex.calories_burned;
    document.getElementById('exercise-duration').value    = ex.duration_minutes;
    document.getElementById('exercise-logged-at').value   = ex.logged_at.slice(0, 16);
    openModal('exercise-modal-overlay');
  } catch (e) {
    toast('Erro ao carregar exercício: ' + e.message, 'error');
  }
};

window._deleteExercise = async (id, name) => {
  const ok = await confirm(`Deseja deletar o exercício "${name}"?`);
  if (!ok) return;
  try {
    await ExerciseAPI.delete(id);
    toast('Exercício deletado!', 'success');
    loadExercises();
  } catch (e) {
    toast('Erro ao deletar: ' + e.message, 'error');
  }
};

async function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('exercise-submit-btn');
  btnLoading(btn, true);

  const payload = {
    name:             document.getElementById('exercise-name').value.trim(),
    description:      document.getElementById('exercise-desc').value.trim() || null,
    calories_burned:  parseFloat(document.getElementById('exercise-calories').value),
    duration_minutes: parseFloat(document.getElementById('exercise-duration').value),
    logged_at:        document.getElementById('exercise-logged-at').value,
  };

  try {
    if (editingId) {
      await ExerciseAPI.update(editingId, payload);
      toast('Exercício atualizado!', 'success');
    } else {
      await ExerciseAPI.create(payload);
      toast('Exercício registrado!', 'success');
    }
    closeModal('exercise-modal-overlay');
    loadExercises();
  } catch (e) {
    toast('Erro: ' + e.message, 'error');
  } finally {
    btnLoading(btn, false);
  }
}

function esc(str) {
  return String(str).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}
