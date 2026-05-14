/**
 * weight.js — Weight log CRUD page
 */

import { WeightAPI }                                     from './api.js';
import { toast, confirm, openModal, closeModal,
         setLoading, setEmpty, formatDate,
         nowLocalISO, btnLoading }                        from './ui.js';
import { renderWeightChart }                              from './chart.js';

let editingId = null;

export function initWeight() {
  document.getElementById('btn-add-weight').addEventListener('click', () => openAddModal());
  document.getElementById('weight-form').addEventListener('submit', handleSubmit);
  document.getElementById('weight-filter-date').addEventListener('change', loadWeightLogs);
  document.getElementById('btn-clear-weight-filter').addEventListener('click', () => {
    document.getElementById('weight-filter-date').value = '';
    loadWeightLogs();
  });
  loadWeightLogs();
}

async function loadWeightLogs() {
  const tbody   = document.getElementById('weight-tbody');
  const dateVal = document.getElementById('weight-filter-date').value;
  setLoading(tbody, 'Carregando registros...');
  try {
    const logs = await WeightAPI.list(dateVal);
    renderTable(logs);
    // Always load full history for chart
    const allLogs = dateVal ? await WeightAPI.list() : logs;
    renderWeightChart('weightChartPage', allLogs);
  } catch (e) {
    toast('Erro ao carregar pesos: ' + e.message, 'error');
    setEmpty(tbody, 'Erro ao carregar dados.');
  }
}

function renderTable(logs) {
  const tbody = document.getElementById('weight-tbody');
  if (!logs.length) { setEmpty(tbody, 'Nenhum registro de peso encontrado.'); return; }

  const sorted = [...logs].sort((a, b) => new Date(b.logged_at) - new Date(a.logged_at));
  tbody.innerHTML = sorted.map((log, i) => {
    const prev  = sorted[i + 1];
    let trend   = '';
    if (prev) {
      const diff = log.weight_kg - prev.weight_kg;
      if      (diff > 0)  trend = `<span class="badge badge-red">▲ +${diff.toFixed(1)} kg</span>`;
      else if (diff < 0)  trend = `<span class="badge badge-green">▼ ${diff.toFixed(1)} kg</span>`;
      else                trend = `<span class="badge badge-yellow">= Estável</span>`;
    }
    return `
    <tr>
      <td><strong>${log.weight_kg.toFixed(1)} kg</strong></td>
      <td>${trend || '<span class="badge badge-purple">— Inicial</span>'}</td>
      <td style="color:var(--text-secondary);font-size:.8rem">${formatDate(log.logged_at)}</td>
      <td>
        <div style="display:flex;gap:6px">
          <button class="btn btn-ghost btn-sm btn-icon" onclick="window._editWeight(${log.id})" title="Editar">✏️</button>
          <button class="btn btn-danger btn-sm btn-icon" onclick="window._deleteWeight(${log.id})" title="Deletar">🗑️</button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

function openAddModal() {
  editingId = null;
  document.getElementById('weight-modal-title').textContent = 'Novo Registro de Peso';
  document.getElementById('weight-form').reset();
  document.getElementById('weight-logged-at').value = nowLocalISO();
  openModal('weight-modal-overlay');
}

window._editWeight = async (id) => {
  try {
    const log = await WeightAPI.get(id);
    editingId = id;
    document.getElementById('weight-modal-title').textContent = 'Editar Registro';
    document.getElementById('weight-kg').value       = log.weight_kg;
    document.getElementById('weight-logged-at').value = log.logged_at.slice(0, 16);
    openModal('weight-modal-overlay');
  } catch (e) {
    toast('Erro ao carregar registro: ' + e.message, 'error');
  }
};

window._deleteWeight = async (id) => {
  const ok = await confirm('Deseja deletar este registro de peso?');
  if (!ok) return;
  try {
    await WeightAPI.delete(id);
    toast('Registro deletado!', 'success');
    loadWeightLogs();
  } catch (e) {
    toast('Erro ao deletar: ' + e.message, 'error');
  }
};

async function handleSubmit(e) {
  e.preventDefault();
  const btn = document.getElementById('weight-submit-btn');
  btnLoading(btn, true);

  const payload = {
    weight_kg:  parseFloat(document.getElementById('weight-kg').value),
    logged_at:  document.getElementById('weight-logged-at').value,
  };

  try {
    if (editingId) {
      await WeightAPI.update(editingId, payload);
      toast('Registro atualizado!', 'success');
    } else {
      await WeightAPI.create(payload);
      toast('Peso registrado!', 'success');
    }
    closeModal('weight-modal-overlay');
    loadWeightLogs();
  } catch (e) {
    toast('Erro: ' + e.message, 'error');
  } finally {
    btnLoading(btn, false);
  }
}
