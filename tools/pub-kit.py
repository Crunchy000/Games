#!/usr/bin/env python3
"""Copy the Bear & Bean pub kit into every game page that uses it.

A page opts in by containing <style id="pub-kit"></style> (for the CSS),
<script id="pub-kit-canvas"></script> (for the canvas helpers) and/or
<script id="pub-kit-settings"></script> (window.BB: the sound and theme settings shared by every game, and
BB.home(): back to all the games, asking "Leave this game?" first whenever BB.leaveRisk() says a game in progress
would be lost; a game that saves everything leaves BB.leaveRisk unset). <script id="pub-kit-steps"></script> turns .pk-steps help into a carousel. Re-run this after
editing tools/pub-kit.css or tools/pub-kit-canvas.js, then run tools/update-sw.py.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / 'tools' / 'pub-kit.css').read_text().strip()
JS = (ROOT / 'tools' / 'pub-kit-canvas.js').read_text().strip()
# one set of house settings shared by every game: sound on/off and light/dark
SETTINGS = """window.BB = (() => {
  const KEY = 'bearbean-settings'; let s = {};
  try { s = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  const put = () => { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {} };
  return {
    get muted() { return 'muted' in s ? !!s.muted : null; }, set muted(v) { s.muted = !!v; put(); },
    get theme() { return s.theme || null; }, set theme(v) { if (v) s.theme = v; else delete s.theme; put(); },
    // going back to all the games: a game sets BB.leaveRisk to a function that says whether a game in progress would be
    // lost; if it would, BB.home() (and any link back home) asks first. BB.asking is true while the question is up, so a
    // game that runs on its own can pause.
    leaveRisk: null, asking: false,
    home(href = '../') { if (BB.leaveRisk && BB.leaveRisk()) askLeave(href); else location.href = href; },
  };
})();
function askLeave(href, byBack) {
  let d = document.getElementById('pk-leave');
  if (!d) {
    d = document.createElement('div'); d.id = 'pk-leave'; d.className = 'pk-leave';
    d.innerHTML = '<div class="pk-card pk-leave-card" role="alertdialog" aria-modal="true" aria-labelledby="pk-leave-t" aria-describedby="pk-leave-d">'
      + '<h2 id="pk-leave-t">Leave this game?</h2><p id="pk-leave-d">The game you\u2019re playing won\u2019t be saved.</p>'
      + '<div class="pk-leave-row"><button type="button" class="pk-btn pk-small" data-stay>Keep playing</button><button type="button" class="pk-btn pk-alt pk-small" data-go>Leave</button></div></div>';
    document.body.appendChild(d);
    const close = () => { d.classList.remove('show'); BB.asking = false; armBack(); };   // staying: the back gesture is guarded again
    const go = () => {
      if (d.dataset.back !== '1') { location.href = d.dataset.href; return; }
      // came by the back gesture: carry on back, or home if there's nowhere to go back to
      const t = setTimeout(() => { location.href = d.dataset.href; }, 500); addEventListener('pagehide', () => clearTimeout(t), { once: true }); history.back();
    };
    d.addEventListener('pointerdown', e => e.stopPropagation());
    d.addEventListener('click', e => { e.stopPropagation(); if (performance.now() - d.opened < 400) return;   // the tap that opened it
      if (e.target === d || e.target.closest('[data-stay]')) close(); else if (e.target.closest('[data-go]')) go(); });
    addEventListener('keydown', e => { if (e.key === 'Escape' && d.classList.contains('show')) { e.stopPropagation(); close(); } }, true);
  }
  d.dataset.href = href; d.dataset.back = byBack ? '1' : ''; d.opened = performance.now(); d.classList.add('show'); BB.asking = true; d.querySelector('[data-stay]').focus();
}
// the phone's back gesture (or back button): a game page keeps one extra history entry, so going back lands here first.
// It's added on a tap, because browsers skip entries added without one. Landing on it with a game in progress asks the
// same question; with nothing to lose it simply carries on back.
let backArmed = false;
function armBack() {
  const d = document.getElementById('pk-leave');
  if (backArmed || (d && d.classList.contains('show'))) return;
  try { history.pushState({ bbStay: 1 }, ''); backArmed = true; } catch (e) {}
}
['pointerup', 'keydown'].forEach(t => addEventListener(t, armBack, true));
addEventListener('popstate', e => {
  if (e.state && e.state.bbStay) { backArmed = true; return; }   // forward again onto the extra entry
  backArmed = false;
  if (BB.leaveRisk && BB.leaveRisk()) { askLeave('../', true); return; }
  const t = setTimeout(() => { location.href = '../'; }, 500); addEventListener('pagehide', () => clearTimeout(t), { once: true }); history.back();
});
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href="../"]');
  if (a && BB.leaveRisk && BB.leaveRisk()) { e.preventDefault(); askLeave(a.getAttribute('href')); }
}, true);"""
# picks a fresh line for each .pk-says panel whenever it comes into view
SAYS = """(() => { const pick = el => { try { const l = JSON.parse(el.dataset.lines || '[]'); if (l.length) el.querySelector('span').textContent = l[Math.floor(Math.random() * l.length)]; } catch (e) {} };
  const go = () => { const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => e.isIntersecting && pick(e.target))) : null; document.querySelectorAll('.pk-says').forEach(el => { pick(el); if (io) io.observe(el); }); };
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', go) : go(); })();"""

# turns each .pk-steps help into a carousel (see tools/pub-kit.css): dots, Back/Skip, Next, swipe and arrow keys; the
# button in the row after it moves onto the last step, and the carousel starts from the first step each time it opens
STEPS = """(() => { const go = () => document.querySelectorAll('.pk-steps').forEach(el => {
  if (el.dataset.ready) return; el.dataset.ready = '1';
  const steps = [...el.children].filter(c => c.classList.contains('pk-step')), n = steps.length; if (n < 2) { steps.forEach(s => s.classList.add('on')); return; }
  const row = el.nextElementSibling, finish = row && row.querySelector('button');
  const mk = (tag, cls, txt) => { const b = document.createElement(tag); if (tag === 'button') b.type = 'button'; b.className = cls; if (txt) b.textContent = txt; return b; };
  const nav = mk('div', 'pk-steps-nav'), back = mk('button', 'pk-steps-back'), dots = mk('div', 'pk-dots'), right = mk('div', 'pk-steps-go'), next = mk('button', 'pk-btn pk-small', 'Next');
  if (!finish) next.classList.add('pk-alt');   // a title screen keeps its own Start button below
  steps.forEach((s, i) => { const d = mk('button', ''); d.setAttribute('aria-label', `Step ${i + 1} of ${n}`); d.onclick = () => show(i); dots.appendChild(d); });
  right.appendChild(next);
  if (finish) { finish.classList.add('pk-small'); right.appendChild(finish); if (!row.querySelector('button, a, input')) row.remove(); }
  nav.append(back, dots, right); el.after(nav);
  let at = 0;
  function show(i) {
    at = Math.max(0, Math.min(n - 1, i));
    steps.forEach((s, k) => { s.classList.toggle('on', k === at); s.classList.toggle('before', k < at); s.setAttribute('aria-hidden', k !== at); s.inert = k !== at; });
    [...dots.children].forEach((d, k) => d.setAttribute('aria-current', k === at ? 'step' : 'false'));
    back.textContent = at ? 'Back' : 'Skip'; back.hidden = !at && !finish;
    next.hidden = at === n - 1; if (finish) finish.hidden = at !== n - 1;
  }
  back.onclick = () => at ? show(at - 1) : finish && finish.click();
  next.onclick = () => show(at + 1);
  let x0 = null;
  el.addEventListener('pointerdown', e => { x0 = e.clientX; });
  el.addEventListener('pointerup', e => { if (x0 === null) return; const dx = e.clientX - x0; x0 = null; if (Math.abs(dx) > 40) show(at + (dx < 0 ? 1 : -1)); });
  addEventListener('keydown', e => { if (!el.offsetParent) return; if (e.key === 'ArrowRight') { show(at + 1); e.preventDefault(); } else if (e.key === 'ArrowLeft') { show(at - 1); e.preventDefault(); } });
  const box = el.closest('.ov') || el.parentElement; let open = false;
  new MutationObserver(() => { const o = !!el.offsetParent; if (o && !open) show(0); open = o; }).observe(box, { attributes: true, attributeFilter: ['class', 'style', 'hidden'] });
  open = !!el.offsetParent; show(0);
});
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', go) : go(); })();"""


def apply(html):
    html = re.sub(r'<style id="pub-kit">.*?</style>', lambda m: '<style id="pub-kit">\n' + CSS + '\n</style>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-canvas">.*?</script>', lambda m: '<script id="pub-kit-canvas">\n' + JS + '\n</script>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-settings">.*?</script>', lambda m: '<script id="pub-kit-settings">\n' + SETTINGS + '\n</script>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-says">.*?</script>', lambda m: '<script id="pub-kit-says">\n' + SAYS + '\n</script>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-steps">.*?</script>', lambda m: '<script id="pub-kit-steps">\n' + STEPS + '\n</script>', html, flags=re.S)
    return html


def main():
    n = 0
    for f in sorted([ROOT / 'index.html'] + list(ROOT.glob('*/index.html'))):
        s = f.read_text()
        t = apply(s)
        if t != s:
            f.write_text(t); n += 1
            print('updated', f.relative_to(ROOT))
    print(n, 'page(s) updated')


if __name__ == '__main__':
    main()
