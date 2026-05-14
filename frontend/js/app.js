/**
 * app.js — Application entry point
 * Handles navigation, sidebar, and page initialization.
 */

import { initDashboard }  from './dashboard.js';
import { initMeals }      from './meals.js';
import { initExercises }  from './exercises.js';
import { initWeight }     from './weight.js';
import { closeModal }     from './ui.js';

const pages = {
  dashboard: { init: initDashboard, initialized: false },
  meals:     { init: initMeals,     initialized: false },
  exercises: { init: initExercises, initialized: false },
  weight:    { init: initWeight,    initialized: false },
};

// ─── Navigation ───────────────────────────────────────────────
function navigate(pageId) {
  // Deactivate all
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  // Activate target
  const pageEl = document.getElementById(`page-${pageId}`);
  if (pageEl) pageEl.classList.add('active');

  const navEl = document.querySelector(`[data-page="${pageId}"]`);
  if (navEl) navEl.classList.add('active');

  // Update topbar title
  const titles = {
    dashboard: '📊 Dashboard',
    meals:     '🍽️ Refeições',
    exercises: '🏋️ Exercícios',
    weight:    '⚖️ Peso Corporal',
  };
  const topbarTitle = document.getElementById('topbar-title');
  if (topbarTitle) topbarTitle.textContent = titles[pageId] || 'BioRitmo';

  // Init page once
  const page = pages[pageId];
  if (page && !page.initialized) {
    page.init();
    page.initialized = true;
  }

  // Close sidebar on mobile
  closeSidebar();
}

// ─── Sidebar mobile ───────────────────────────────────────────
function openSidebar() {
  document.querySelector('.sidebar').classList.add('open');
  document.querySelector('.sidebar-mask').classList.add('open');
}

function closeSidebar() {
  document.querySelector('.sidebar').classList.remove('open');
  document.querySelector('.sidebar-mask').classList.remove('open');
}

// ─── Modal close buttons ──────────────────────────────────────
function setupModalCloseButtons() {
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.closeModal));
  });

  // Close on overlay click
  document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) closeModal(overlay.id);
    });
  });
}

// ─── Date display ─────────────────────────────────────────────
function setTodayDate() {
  const el = document.getElementById('today-date');
  if (!el) return;
  el.textContent = new Date().toLocaleDateString('pt-BR', {
    weekday: 'short', day: '2-digit', month: 'short', year: 'numeric',
  });
}

// ─── Boot ─────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  setTodayDate();

  // Nav click handlers
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => navigate(item.dataset.page));
  });

  // Sidebar burger
  document.getElementById('burger-btn')?.addEventListener('click', openSidebar);
  document.querySelector('.sidebar-mask')?.addEventListener('click', closeSidebar);

  setupModalCloseButtons();

  // Start on dashboard
  navigate('dashboard');
});
