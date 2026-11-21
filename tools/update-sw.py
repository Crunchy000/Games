#!/usr/bin/env python3
"""Rebuild sw.js so the offline app knows about every game.

Run from anywhere:  python3 tools/update-sw.py
It lists the home page, every folder with an index.html (plus any pictures kept beside it), the manifest and the icons, and stamps
a version made from their contents. When anything changes the version changes, so installed
copies download the new set in the background and switch over in one go.
"""
import hashlib, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
games = sorted(p.parent.name for p in root.glob('*/index.html') if p.parent.name not in ('tools', 'icons'))
files = ['./', './manifest.webmanifest'] + [f'./icons/{p.name}' for p in sorted(p for p in (root / 'icons').iterdir() if p.suffix in ('.png', '.jpg', '.webp', '.svg'))] + [f'./{g}/' for g in games]
# pictures a game keeps next to its page (e.g. hide-and-seek/camp.webp) are saved for offline play too
ASSET = ('.png', '.jpg', '.webp', '.svg')
assets = [f'{g}/{p.name}' for g in games for p in sorted((root / g).iterdir()) if p.suffix in ASSET]
# big pictures (over 60 KB) aren't downloaded up front for every visitor: the game that uses them saves them for
# offline play when it's opened. They still count towards the version, so changes to them roll out.
files += [f'./{a}' for a in assets if (root / a).stat().st_size <= 60 * 1024]
h = hashlib.sha256()
for f in ['index.html', 'manifest.webmanifest'] + [f'icons/{p.name}' for p in sorted(p for p in (root / 'icons').iterdir() if p.suffix in ('.png', '.jpg', '.webp', '.svg'))] + [f'{g}/index.html' for g in games] + assets:
    h.update((root / f).read_bytes())
version = 'games-' + h.hexdigest()[:12]
template = (root / 'tools' / 'sw-template.js').read_text()
(root / 'sw.js').write_text(template.replace('__VERSION__', version).replace('__FILES__', ',\n  '.join(repr(f) for f in files)))
print(f'sw.js: {version}, {len(files)} files ({len(games)} games)')
