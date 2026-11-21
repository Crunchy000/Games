#!/usr/bin/env python3
"""Stamp asset addresses and rebuild sw.js so the offline app knows about every game.

Run from anywhere:  python3 tools/update-sw.py

1. Every icon and every picture kept beside a game page gets a fingerprint of its contents. Pages are rewritten so
   they ask for e.g. ../icons/bear.png?v=3fa2c1d0, and a page with <script id="asset-versions"></script> gets a
   window.AV list of the stamps for its own pictures (for addresses it builds in code). Change a file and its
   address changes, so no cache anywhere (the phone, the offline copy, Cloudflare) can hand out the old one.
2. sw.js lists the home page, every game page, the manifest, the icons and the small pictures, and carries a version
   made from all of their contents. When anything changes the version changes, so installed copies fetch the new
   set and switch over in one go.
"""
import hashlib, json, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
PIC = ('.png', '.jpg', '.webp', '.svg')
games = sorted(p.parent.name for p in root.glob('*/index.html') if p.parent.name not in ('tools', 'icons'))
stamp = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()[:8]
icons = {p.name: stamp(p) for p in sorted((root / 'icons').iterdir()) if p.suffix in PIC}
assets = {g: {p.name: stamp(p) for p in sorted((root / g).iterdir()) if p.suffix in PIC} for g in games}

# ---- 1. stamp the pages (and the manifest) ----
ICON_REF = re.compile(r'((?:\.\./)?icons/([\w.-]+\.(?:png|jpg|webp|svg)))(\?v=[0-9a-f]+)?')
def stamp_icons(text):
    return ICON_REF.sub(lambda m: m.group(1) + (f'?v={icons[m.group(2)]}' if m.group(2) in icons else (m.group(3) or '')), text)
AV = re.compile(r'(<script id="asset-versions">)(.*?)(</script>)', re.S)
changed = 0
for page, folder in [(root / 'index.html', None)] + [(root / g / 'index.html', g) for g in games]:
    s = page.read_text(); new = stamp_icons(s)
    if folder and AV.search(new):
        new = AV.sub(lambda m: m.group(1) + 'window.AV = ' + json.dumps(assets[folder], separators=(',', ':')) + ';' + m.group(3), new)
    if new != s: page.write_text(new); changed += 1
man = root / 'manifest.webmanifest'; ms = man.read_text(); mnew = stamp_icons(ms)
if mnew != ms: man.write_text(mnew); changed += 1

# ---- 2. the offline list and its version ----
files = ['./', './manifest.webmanifest'] + [f'./icons/{n}?v={v}' for n, v in icons.items()] + [f'./{g}/' for g in games]
# big pictures (over 60 KB) aren't downloaded up front for every visitor: the game that uses them saves them for
# offline play when it's opened. They still count towards the version, so changes to them roll out.
files += [f'./{g}/{n}?v={v}' for g in games for n, v in assets[g].items() if (root / g / n).stat().st_size <= 60 * 1024]
h = hashlib.sha256()
for f in ['index.html', 'manifest.webmanifest'] + [f'{g}/index.html' for g in games]:
    h.update((root / f).read_bytes())
for v in list(icons.values()) + [v for g in games for v in assets[g].values()]:
    h.update(v.encode())
version = 'games-' + h.hexdigest()[:12]
template = (root / 'tools' / 'sw-template.js').read_text()
(root / 'sw.js').write_text(template.replace('__VERSION__', version).replace('__FILES__', ',\n  '.join(repr(f) for f in files)))
print(f'sw.js: {version}, {len(files)} files ({len(games)} games); {changed} page(s) re-stamped')
