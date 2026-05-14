/**
 * dashboard.js — Dashboard page logic
 */

import { DashboardAPI, WeightAPI } from './api.js';
import { toast, todayISO }         from './ui.js';
import { renderWeightChart }        from './chart.js';

export async function initDashboard() {
  const dateInput = document.getElementById('dash-date');
  if (dateInput) {
    dateInput.value = todayISO();
    dateInput.addEventListener('change', loadDashboard);
  }
  await loadDashboard();
}

async function loadDashboard() {
  const dateInput = document.getElementById('dash-date');
  const date = dateInput?.value || todayISO();

  try {
    const [summary, weightLogs] = await Promise.all([
      DashboardAPI.summary(date),
      WeightAPI.list(),
    ]);
    renderSummaryCards(summary);
    renderWeightChart('weightChart', weightLogs);
  } catch (e) {
    toast('Erro ao carregar dashboard: ' + e.message, 'error');
  }
}

function renderSummaryCards(s) {
  // Caloric balance
  const balance = s.caloric_balance;
  const balClass = balance > 0 ? 'balance-positive' : balance < 0 ? 'balance-negative' : 'balance-neutral';
  const balSign  = balance > 0 ? '+' : '';

  setText('dash-consumed',  `${s.total_calories_consumed.toFixed(0)} kcal`);
  setText('dash-burned',    `${s.total_calories_burned.toFixed(0)} kcal`);
  setText('dash-meals',     s.meal_count);
  setText('dash-exercises', s.exercise_count);

  const balEl = document.getElementById('dash-balance');
  if (balEl) {
    balEl.textContent = `${balSign}${balance.toFixed(0)} kcal`;
    balEl.className   = `card-value ${balClass}`;
  }

  // Water progress
  setText('dash-water-consumed', `${(s.total_water_ml / 1000).toFixed(2)} L`);
  setText('dash-water-goal',     `Meta: ${(s.water_goal_ml / 1000).toFixed(1)} L`);
  setText('dash-water-remaining', `Restam: ${Math.max(0, (s.water_goal_ml - s.total_water_ml) / 1000).toFixed(2)} L`);
  setText('dash-water-pct',      `${s.water_progress_pct}%`);

  const fill = document.getElementById('water-fill');
  if (fill) {
    fill.style.width = `${Math.min(s.water_progress_pct, 100)}%`;
    fill.className = 'progress-fill ' + (
      s.water_progress_pct >= 100 ? 'green' :
      s.water_progress_pct >= 50  ? 'blue'  : 'yellow'
    );
  }
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
