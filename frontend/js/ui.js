/**
 * ui.js — Shared UI utilities: toasts, modals, loaders, confirm dialogs
 */

// ─── Toast ────────────────────────────────────────────────────
export function toast(message, type = 'info', duration = 3500) {
  const container = document.getElementById('toast-container');
  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };

  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${icons[type] ?? 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(el);

  setTimeout(() => {
    el.classList.add('leaving');
    el.addEventListener('animationend', () => el.remove());
  }, duration);
}

// ─── Modal ────────────────────────────────────────────────────
export function openModal(overlayId) {
  const el = document.getElementById(overlayId);
  if (el) el.classList.add('open');
}

export function closeModal(overlayId) {
  const el = document.getElementById(overlayId);
  if (el) el.classList.remove('open');
}

// ─── Confirm dialog ───────────────────────────────────────────
export function confirm(message) {
  return new Promise((resolve) => {
    const overlay = document.getElementById('confirm-overlay');
    const msgEl   = document.getElementById('confirm-message');
    const yesBtn  = document.getElementById('confirm-yes');
    const noBtn   = document.getElementById('confirm-no');

    msgEl.textContent = message;
    overlay.classList.add('open');

    const cleanup = (result) => {
      overlay.classList.remove('open');
      yesBtn.replaceWith(yesBtn.cloneNode(true));
      noBtn.replaceWith(noBtn.cloneNode(true));
      resolve(result);
    };

    document.getElementById('confirm-yes').addEventListener('click', () => cleanup(true),  { once: true });
    document.getElementById('confirm-no').addEventListener('click',  () => cleanup(false), { once: true });
  });
}

// ─── Loading state helpers ────────────────────────────────────
export function setLoading(container, message = 'Carregando...') {
  container.innerHTML = `
    <div class="loading-state">
      <div class="spinner"></div>
      <span>${message}</span>
    </div>`;
}

export function setEmpty(container, message = 'Nenhum registro encontrado.') {
  container.innerHTML = `
    <div class="empty-state">
      <div class="empty-icon">📭</div>
      <p>${message}</p>
    </div>`;
}

// ─── Format helpers ────────────────────────────────────────────
export function formatDate(isoString) {
  if (!isoString) return '—';
  const d = new Date(isoString);
  return d.toLocaleString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit',
  });
}

export function formatDateShort(isoString) {
  if (!isoString) return '—';
  const d = new Date(isoString);
  return d.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
}

export function todayISO() {
  return new Date().toISOString().split('T')[0];
}

export function nowLocalISO() {
  const now = new Date();
  const offset = now.getTimezoneOffset() * 60000;
  return new Date(now - offset).toISOString().slice(0, 16);
}

// ─── Set btn loading state ────────────────────────────────────
export function btnLoading(btn, loading) {
  if (loading) {
    btn.dataset.original = btn.innerHTML;
    btn.innerHTML = '<span class="spinner"></span>';
    btn.disabled = true;
  } else {
    btn.innerHTML = btn.dataset.original || btn.innerHTML;
    btn.disabled = false;
  }
}
