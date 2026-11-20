/* The Bear & Bean house style for canvas games: soft clay, drawn with a 2D context.
   tools/pub-kit.py copies this into each canvas game that uses it. */
window.PK = (() => {
  const CLAY = '#c8643b', CLAY_LO = '#a94f2c', SAGE = '#dce3d3', SAGE_INK = '#3f4e35', SAGE_LO = '#c3ccb8';
  const CARD = '#f7f1e7', CARD_2 = '#efe5d6', INK = '#3b2e22', INK_2 = '#6e6152', INK_3 = '#8e7f6c', ON_CLAY = '#fff5ec', CLAY_TEXT = '#b5532e';
  const SLAB = '"ui-rounded","SF Pro Rounded","Nunito","Varela Round","Segoe UI",system-ui,-apple-system,Roboto,sans-serif';
  function rr(g, x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
  // a rounded button centred on (x, y); alt = sage
  function plank(g, x, y, w, h, label, opt = {}) {
    const x0 = x - w / 2, y0 = y - h / 2 + (opt.pressed ? 2 : 0), r = Math.min(16, h / 2);
    g.save();
    g.fillStyle = opt.alt ? 'rgba(60,75,45,.14)' : 'rgba(120,55,25,.2)'; rr(g, x0, y0 + 6, w, h, r); g.fill();
    g.fillStyle = opt.alt ? SAGE_LO : CLAY_LO; rr(g, x0, y0 + 2, w, h, r); g.fill();
    g.fillStyle = opt.alt ? SAGE : CLAY; rr(g, x0, y0, w, h, r); g.fill();
    g.font = `700 ${opt.size || 17}px ${SLAB}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillStyle = opt.alt ? SAGE_INK : ON_CLAY; g.fillText(label, x, y0 + h / 2 + 1);
    g.restore();
  }
  // a soft cream card
  function board(g, x, y, w, h) {
    g.save();
    g.fillStyle = 'rgba(50,30,12,.16)'; rr(g, x + 1, y + 10, w - 2, h, 24); g.fill();
    g.fillStyle = 'rgba(50,30,12,.1)'; rr(g, x, y + 3, w, h, 24); g.fill();
    g.fillStyle = CARD; rr(g, x, y, w, h, 24); g.fill();
    g.restore();
  }
  // a small rounded square button with an icon drawn by fn(g, cx, cy)
  function sign(g, x, y, w, h, fn) {
    g.save();
    g.fillStyle = 'rgba(50,30,12,.18)'; rr(g, x, y + 3, w, h, 13); g.fill();
    g.fillStyle = CARD; rr(g, x, y, w, h, 13); g.fill();
    g.strokeStyle = INK; g.fillStyle = INK; g.lineWidth = 2; g.lineJoin = 'round'; g.lineCap = 'round';
    if (fn) fn(g, x + w / 2, y + h / 2);
    g.restore();
  }
  function house(g, cx, cy) { g.beginPath(); g.moveTo(cx - 8, cy); g.lineTo(cx, cy - 7); g.lineTo(cx + 8, cy); g.moveTo(cx - 5.5, cy - 2); g.lineTo(cx - 5.5, cy + 7); g.lineTo(cx + 5.5, cy + 7); g.lineTo(cx + 5.5, cy - 2); g.stroke(); }
  function homeSign(g, x, y, w = 38, h = 38) { sign(g, x, y, w, h, house); }
  // "THE BEAR & BEAN PRESENTS" with both faces
  function presents(g, x, y, imgs, opt = {}) {
    const s = opt.size || 10, txt = (opt.text || 'THE BEAR & BEAN PRESENTS').split('').join(String.fromCharCode(8202));
    g.save(); g.font = `700 ${s}px ${SLAB}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    const tw = g.measureText(txt).width, r = s * 1.15;
    g.fillStyle = opt.color || INK_3; g.fillText(txt, x, y);
    if (imgs) [[imgs[0], x - tw / 2 - r - 6], [imgs[1], x + tw / 2 + r + 6]].forEach(([im, cx]) => face(g, im, cx, y, r));
    g.restore();
  }
  function face(g, im, cx, cy, r) {
    g.save(); g.fillStyle = 'rgba(60,35,15,.22)'; g.beginPath(); g.arc(cx, cy + 1, r + 2, 0, 6.2832); g.fill();
    g.fillStyle = '#fff'; g.beginPath(); g.arc(cx, cy, r + 2, 0, 6.2832); g.fill();
    if (im && im.complete && im.naturalWidth) { g.beginPath(); g.arc(cx, cy, r, 0, 6.2832); g.clip(); g.drawImage(im, cx - r, cy - r, r * 2, r * 2); }
    g.restore();
  }
  // a word from Bear or Bean
  function says(g, x, y, w, im, who, line, opt = {}) {
    g.save(); const h = 54;
    g.fillStyle = CARD_2; rr(g, x, y, w, h, 16); g.fill();
    face(g, im, x + 30, y + h / 2, 18);
    g.textAlign = 'left'; g.textBaseline = 'middle';
    g.font = `700 10px ${SLAB}`; g.fillStyle = CLAY_TEXT; g.fillText(who.toUpperCase() + ' SAYS', x + 58, y + 17);
    g.font = `700 ${opt.size || 14}px ${SLAB}`; g.fillStyle = INK; g.fillText(line, x + 58, y + 36);
    g.restore();
  }
  // CREAM and CREAM_DIM are the text colours to use on a card (named before the restyle)
  return { plank, board, sign, homeSign, house, presents, face, says, rr, SLAB, CREAM: INK, CREAM_DIM: INK_2, INK, INK_2, INK_3, CLAY, CLAY_TEXT, CARD, BRASS: CLAY_TEXT };
})();
