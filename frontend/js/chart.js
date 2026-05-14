/**
 * chart.js — Pure JS/Canvas weight evolution chart
 * No external libraries used.
 */

export function renderWeightChart(canvasId, logs) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  // DPI scaling
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.parentElement.getBoundingClientRect();
  canvas.width  = rect.width  * dpr;
  canvas.height = rect.height * dpr;
  ctx.scale(dpr, dpr);
  const W = rect.width;
  const H = rect.height;

  ctx.clearRect(0, 0, W, H);

  if (!logs || logs.length === 0) {
    ctx.fillStyle = '#555c73';
    ctx.font = '14px Inter, system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Nenhum registro de peso ainda.', W / 2, H / 2);
    return;
  }

  // Sort by date
  const sorted = [...logs].sort((a, b) => new Date(a.logged_at) - new Date(b.logged_at));
  const weights = sorted.map(l => l.weight_kg);
  const labels  = sorted.map(l => {
    const d = new Date(l.logged_at);
    return `${String(d.getDate()).padStart(2,'0')}/${String(d.getMonth()+1).padStart(2,'0')}`;
  });

  const minW  = Math.min(...weights);
  const maxW  = Math.max(...weights);
  const range = maxW - minW || 1;
  const pad   = { top: 20, right: 20, bottom: 36, left: 48 };
  const chartW = W - pad.left - pad.right;
  const chartH = H - pad.top  - pad.bottom;

  const xStep = sorted.length > 1 ? chartW / (sorted.length - 1) : chartW;
  const toX = (i)   => pad.left + (sorted.length > 1 ? i * xStep : chartW / 2);
  const toY = (val) => pad.top  + chartH - ((val - minW) / range) * chartH;

  // ─── Grid lines ──────────────────────────────────────────────
  const gridLines = 4;
  ctx.strokeStyle = '#252a38';
  ctx.lineWidth = 1;
  for (let i = 0; i <= gridLines; i++) {
    const y = pad.top + (chartH / gridLines) * i;
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(W - pad.right, y);
    ctx.stroke();

    const val = maxW - (range / gridLines) * i;
    ctx.fillStyle = '#555c73';
    ctx.font = '11px Inter, system-ui, sans-serif';
    ctx.textAlign = 'right';
    ctx.fillText(`${val.toFixed(1)}`, pad.left - 6, y + 4);
  }

  // ─── Gradient area ────────────────────────────────────────────
  const grad = ctx.createLinearGradient(0, pad.top, 0, pad.top + chartH);
  grad.addColorStop(0,   'rgba(108,99,255,.35)');
  grad.addColorStop(1,   'rgba(108,99,255,.02)');

  ctx.beginPath();
  ctx.moveTo(toX(0), toY(weights[0]));
  for (let i = 1; i < sorted.length; i++) {
    const cpX = (toX(i - 1) + toX(i)) / 2;
    ctx.bezierCurveTo(cpX, toY(weights[i-1]), cpX, toY(weights[i]), toX(i), toY(weights[i]));
  }
  ctx.lineTo(toX(sorted.length - 1), pad.top + chartH);
  ctx.lineTo(toX(0), pad.top + chartH);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // ─── Line ─────────────────────────────────────────────────────
  ctx.beginPath();
  ctx.moveTo(toX(0), toY(weights[0]));
  for (let i = 1; i < sorted.length; i++) {
    const cpX = (toX(i - 1) + toX(i)) / 2;
    ctx.bezierCurveTo(cpX, toY(weights[i-1]), cpX, toY(weights[i]), toX(i), toY(weights[i]));
  }
  ctx.strokeStyle = '#6c63ff';
  ctx.lineWidth   = 2.5;
  ctx.lineJoin    = 'round';
  ctx.stroke();

  // ─── Dots & labels ────────────────────────────────────────────
  sorted.forEach((log, i) => {
    const x = toX(i);
    const y = toY(log.weight_kg);

    // Glow
    ctx.beginPath();
    ctx.arc(x, y, 7, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(108,99,255,.25)';
    ctx.fill();

    // Dot
    ctx.beginPath();
    ctx.arc(x, y, 4, 0, Math.PI * 2);
    ctx.fillStyle = '#6c63ff';
    ctx.fill();
    ctx.strokeStyle = '#fff';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // X label (date)
    ctx.fillStyle = '#8b90a4';
    ctx.font = '10px Inter, system-ui, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], x, H - pad.bottom + 18);

    // Value above dot (only if not too crowded)
    if (sorted.length <= 10) {
      ctx.fillStyle = '#e8eaf0';
      ctx.font = 'bold 10px Inter, system-ui, sans-serif';
      ctx.fillText(`${log.weight_kg}kg`, x, y - 12);
    }
  });
}
