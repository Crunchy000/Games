/* The Bear & Bean pub kit for canvas games: the same aged wood, drawn with a 2D context.
   tools/pub-kit.py copies this into each canvas game that uses it. */
window.PK = (() => {
  const OAK = ['#e2b27a', '#c18a52', '#94612f'], WAL = ['#5e3b20', '#47291a', '#2f1a0e'], EDGE = '#221208';
  const CREAM = '#fbefd6', CREAM_DIM = '#dcc5a0', INK = '#2e1a0d', BRASS = '#e5b65a';
  const SLAB = '"Rockwell","Roboto Slab","Zilla Slab","Arvo",Georgia,"Times New Roman",serif';
  function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
  // fine grain lines, seeded by position so they stay still between frames
  function grain(g, x, y, w, h, light) {
    g.save(); rr(g, x, y, w, h, 2); g.clip();
    let s = Math.floor(x * 7 + y * 13 + w) >>> 0; const rnd = () => (s = (s * 1664525 + 1013904223) >>> 0) / 4294967296;
    for (let i = 0; i < h / 3.2; i++) {
      const yy = y + i * 3.2 + rnd() * 2;
      g.strokeStyle = rnd() < .5 ? `rgba(35,15,4,${.06 + rnd() * .08})` : `rgba(255,232,196,${light ? .08 : .04})`;
      g.lineWidth = .8 + rnd(); g.beginPath(); g.moveTo(x, yy); g.bezierCurveTo(x + w * .3, yy + rnd() * 2 - 1, x + w * .7, yy + rnd() * 2 - 1, x + w, yy + rnd() * 1.5); g.stroke();
    }
    if (w > 60) { const kx = x + w * (.2 + rnd() * .6), ky = y + h * (.35 + rnd() * .3); g.fillStyle = 'rgba(70,35,10,.25)'; g.beginPath(); g.ellipse(kx, ky, 7, 2.4, 0, 0, 6.2832); g.fill(); }
    g.restore();
  }
  function nail(g, x, y, r = 2.4) {
    const n = g.createRadialGradient(x - r * .3, y - r * .3, .2, x, y, r); n.addColorStop(0, '#fbe3a6'); n.addColorStop(1, '#a8761f');
    g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.arc(x, y + .8, r, 0, 6.2832); g.fill();
    g.fillStyle = n; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill();
  }
  // a plank button centred on (x, y); alt = dark walnut with cream lettering
  function plank(g, x, y, w, h, label, opt = {}) {
    const x0 = x - w / 2, y0 = y - h / 2 + (opt.pressed ? 2 : 0), c = opt.alt ? WAL : OAK;
    g.save();
    g.fillStyle = 'rgba(0,0,0,.28)'; rr(g, x0, y0 + 5, w, h, 10); g.fill();
    g.fillStyle = EDGE; rr(g, x0, y0 + (opt.pressed ? 1 : 3), w, h, 10); g.fill();
    const gr = g.createLinearGradient(0, y0, 0, y0 + h); gr.addColorStop(0, c[0]); gr.addColorStop(.55, c[1]); gr.addColorStop(1, c[2]);
    g.fillStyle = gr; rr(g, x0, y0, w, h, 10); g.fill();
    grain(g, x0, y0, w, h, !opt.alt);
    g.strokeStyle = 'rgba(40,18,4,.5)'; g.lineWidth = 1; rr(g, x0 + .5, y0 + .5, w - 1, h - 1, 9.5); g.stroke();
    g.strokeStyle = opt.alt ? 'rgba(255,220,170,.18)' : 'rgba(255,240,215,.55)'; g.beginPath(); g.moveTo(x0 + 8, y0 + 1.5); g.lineTo(x0 + w - 8, y0 + 1.5); g.stroke();
    if (w > 90) { nail(g, x0 + 9, y0 + h / 2, 2.3); nail(g, x0 + w - 9, y0 + h / 2, 2.3); }
    g.font = `800 ${opt.size || 18}px ${SLAB}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    if (opt.alt) { g.fillStyle = 'rgba(0,0,0,.6)'; g.fillText(label, x, y0 + h / 2 + 2); g.fillStyle = CREAM; }
    else { g.fillStyle = 'rgba(255,236,204,.55)'; g.fillText(label, x, y0 + h / 2 + 2); g.fillStyle = INK; }
    g.fillText(label, x, y0 + h / 2 + 1);
    g.restore();
  }
  // a framed board: dark stained panel inside an oak frame, nails in the corners
  function board(g, x, y, w, h, opt = {}) {
    const f = opt.frame || 7;
    g.save();
    g.fillStyle = 'rgba(0,0,0,.4)'; rr(g, x + 2, y + 8, w, h, 16); g.fill();
    const fr = g.createLinearGradient(0, y, 0, y + h); fr.addColorStop(0, OAK[0]); fr.addColorStop(1, OAK[2]);
    g.fillStyle = fr; rr(g, x, y, w, h, 16); g.fill(); grain(g, x, y, w, h, true);
    g.fillStyle = EDGE; rr(g, x + f - 1, y + f - 1, w - 2 * f + 2, h - 2 * f + 2, 11); g.fill();
    const pg = g.createLinearGradient(0, y, 0, y + h); pg.addColorStop(0, '#553219'); pg.addColorStop(1, '#3b2112');
    g.fillStyle = opt.alpha != null ? `rgba(70,40,22,${opt.alpha})` : pg; rr(g, x + f, y + f, w - 2 * f, h - 2 * f, 10); g.fill();
    if (opt.alpha == null) grain(g, x + f, y + f, w - 2 * f, h - 2 * f, false);
    const sh = g.createRadialGradient(x + w / 2, y + f, 4, x + w / 2, y + f, w * .7); sh.addColorStop(0, 'rgba(255,210,150,.12)'); sh.addColorStop(1, 'rgba(255,210,150,0)');
    g.fillStyle = sh; rr(g, x + f, y + f, w - 2 * f, h - 2 * f, 10); g.fill();
    for (const [nx, ny] of [[x + f + 6, y + f + 6], [x + w - f - 6, y + f + 6], [x + f + 6, y + h - f - 6], [x + w - f - 6, y + h - f - 6]]) nail(g, nx, ny, 2.2);
    g.restore();
  }
  // a small wooden sign button with an icon drawn by fn(g, cx, cy) in cream
  function sign(g, x, y, w, h, fn) {
    g.save();
    g.fillStyle = 'rgba(0,0,0,.25)'; rr(g, x, y + 3, w, h, 10); g.fill();
    g.fillStyle = EDGE; rr(g, x, y + 2, w, h, 10); g.fill();
    const gr = g.createLinearGradient(0, y, 0, y + h); gr.addColorStop(0, WAL[0]); gr.addColorStop(1, WAL[2]);
    g.fillStyle = gr; rr(g, x, y, w, h, 10); g.fill(); grain(g, x, y, w, h, false);
    g.strokeStyle = 'rgba(0,0,0,.45)'; g.lineWidth = 1; rr(g, x + .5, y + .5, w - 1, h - 1, 9.5); g.stroke();
    g.strokeStyle = CREAM; g.fillStyle = CREAM; g.lineWidth = 2; g.lineJoin = 'round'; g.lineCap = 'round';
    if (fn) fn(g, x + w / 2, y + h / 2);
    g.restore();
  }
  function house(g, cx, cy) { g.beginPath(); g.moveTo(cx - 8, cy); g.lineTo(cx, cy - 7); g.lineTo(cx + 8, cy); g.moveTo(cx - 5.5, cy - 2); g.lineTo(cx - 5.5, cy + 7); g.lineTo(cx + 5.5, cy + 7); g.lineTo(cx + 5.5, cy - 2); g.stroke(); }
  function homeSign(g, x, y, w = 38, h = 38) { sign(g, x, y, w, h, house); }
  // "THE BEAR & BEAN PRESENTS" with both faces
  function presents(g, x, y, imgs, opt = {}) {
    const s = opt.size || 10, txt = opt.text || 'THE BEAR & BEAN PRESENTS';
    g.save(); g.font = `800 ${s}px ${SLAB}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    const tw = g.measureText(txt.split('').join(String.fromCharCode(8202))).width, r = s * 1.15;
    g.fillStyle = opt.color || BRASS; g.fillText(txt.split('').join(String.fromCharCode(8202)), x, y);
    if (imgs) [[imgs[0], x - tw / 2 - r - 6], [imgs[1], x + tw / 2 + r + 6]].forEach(([im, cx]) => face(g, im, cx, y, r));
    g.restore();
  }
  function face(g, im, cx, cy, r, ring = OAK[1]) {
    g.save(); g.fillStyle = ring; g.beginPath(); g.arc(cx, cy, r + 2, 0, 6.2832); g.fill();
    g.fillStyle = '#fff'; g.beginPath(); g.arc(cx, cy, r, 0, 6.2832); g.fill();
    if (im && im.complete && im.naturalWidth) { g.beginPath(); g.arc(cx, cy, r, 0, 6.2832); g.clip(); g.drawImage(im, cx - r, cy - r, r * 2, r * 2); }
    g.restore();
  }
  // a word from Bear or Bean: face plus a two-line speech panel
  function says(g, x, y, w, im, who, line, opt = {}) {
    g.save(); const h = 54;
    g.fillStyle = 'rgba(0,0,0,.25)'; rr(g, x, y, w, h, 12); g.fill();
    g.strokeStyle = 'rgba(255,220,170,.14)'; g.lineWidth = 1; rr(g, x + .5, y + .5, w - 1, h - 1, 12); g.stroke();
    face(g, im, x + 30, y + h / 2, 19);
    g.textAlign = 'left'; g.textBaseline = 'middle';
    g.font = `800 10px ${SLAB}`; g.fillStyle = BRASS; g.fillText(who.toUpperCase() + ' SAYS', x + 58, y + 17);
    g.font = `800 ${opt.size || 14}px system-ui,-apple-system,"Segoe UI",Roboto,sans-serif`; g.fillStyle = CREAM; g.fillText(line, x + 58, y + 36);
    g.restore();
  }
  return { plank, board, sign, homeSign, house, presents, face, says, grain, nail, rr, SLAB, CREAM, CREAM_DIM, INK, BRASS, OAK, WAL };
})();
