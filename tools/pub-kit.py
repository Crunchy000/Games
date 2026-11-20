#!/usr/bin/env python3
"""Copy the Bear & Bean pub kit into every game page that uses it.

A page opts in by containing <style id="pub-kit"></style> (for the CSS),
<script id="pub-kit-canvas"></script> (for the canvas helpers) and/or
<script id="pub-kit-settings"></script> (window.BB: the sound and theme settings shared by every game). Re-run this after
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
  };
})();"""
# picks a fresh line for each .pk-says panel whenever it comes into view
SAYS = """(() => { const pick = el => { try { const l = JSON.parse(el.dataset.lines || '[]'); if (l.length) el.querySelector('span').textContent = l[Math.floor(Math.random() * l.length)]; } catch (e) {} };
  const go = () => { const io = 'IntersectionObserver' in window ? new IntersectionObserver(es => es.forEach(e => e.isIntersecting && pick(e.target))) : null; document.querySelectorAll('.pk-says').forEach(el => { pick(el); if (io) io.observe(el); }); };
  document.readyState === 'loading' ? addEventListener('DOMContentLoaded', go) : go(); })();"""


def apply(html):
    html = re.sub(r'<style id="pub-kit">.*?</style>', lambda m: '<style id="pub-kit">\n' + CSS + '\n</style>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-canvas">.*?</script>', lambda m: '<script id="pub-kit-canvas">\n' + JS + '\n</script>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-settings">.*?</script>', lambda m: '<script id="pub-kit-settings">\n' + SETTINGS + '\n</script>', html, flags=re.S)
    html = re.sub(r'<script id="pub-kit-says">.*?</script>', lambda m: '<script id="pub-kit-says">\n' + SAYS + '\n</script>', html, flags=re.S)
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
