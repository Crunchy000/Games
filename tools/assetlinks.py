#!/usr/bin/env python3
"""Write .well-known/assetlinks.json, the trust link between the Android app and this site.

Usage: python3 tools/assetlinks.py AA:BB:...  [CC:DD:...]
Pass the SHA-256 fingerprint of every key that signs the app: PWABuilder's signing key (in its
zip's assetlinks.json or signing-key-info.txt) and, once the app is on Google Play, the
"App signing key certificate" fingerprint from Play Console > Test and release > App integrity.
Without the right fingerprints the app still opens, but with a browser address bar across the top.
"""
import json, pathlib, re, sys
PACKAGE = 'uk.bearandbean.games'
root = pathlib.Path(__file__).resolve().parent.parent
path = root / '.well-known' / 'assetlinks.json'
old = json.loads(path.read_text())[0]['target']['sha256_cert_fingerprints'] if path.exists() else []
fps = []
for f in old + sys.argv[1:]:
    f = f.strip().upper()
    if not re.fullmatch(r'([0-9A-F]{2}:){31}[0-9A-F]{2}', f): sys.exit(f'Not a SHA-256 fingerprint: {f}')
    if f not in fps: fps.append(f)
path.parent.mkdir(exist_ok=True)
path.write_text(json.dumps([{"relation": ["delegate_permission/common.handle_all_urls"],
  "target": {"namespace": "android_app", "package_name": PACKAGE, "sha256_cert_fingerprints": fps}}], indent=2) + '\n')
print(f'{path.relative_to(root)}: {PACKAGE}, {len(fps)} fingerprint(s)')
