#!/usr/bin/env python3
"""Build-time gates for the exact exported client artifact (Python 3.11+)."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
import tomllib
import urllib.request
import urllib.error
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor


def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError) as exc:
            if isinstance(exc, urllib.error.HTTPError) and exc.code not in (429, 500, 502, 503, 504):
                raise RuntimeError('Public download failed: ' + url + ': ' + str(exc)) from exc
            if attempt == 2:
                raise RuntimeError('Public download failed after 3 attempts: ' + url + ': ' + str(exc)) from exc
            print('Retrying public download:', url, 'attempt', attempt + 2, flush=True)
            time.sleep(2 * (attempt + 1))


def metadata(root):
    result = {}
    for path in root.rglob('*.pw.toml'):
        if any(p in ('.git', 'dist', 'compat', 'backups') for p in path.relative_to(root).parts):
            continue
        data = tomllib.loads(path.read_text())
        if data.get('side', 'both') == 'server':
            continue
        target = (path.parent / data['filename']).relative_to(root).as_posix()
        if target in result:
            raise RuntimeError('Duplicate published destination: ' + target)
        result[target] = data['download']
    return result


def check(root, archive, public=False, payload_root=None):
    expected = metadata(root)
    pack = tomllib.loads((root / 'pack.toml').read_text())
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError('Duplicate ZIP entries')
        index = json.loads(z.read('modrinth.index.json'))
        if index['versionId'] != pack['version']:
            raise RuntimeError('Release version differs from pack.toml')
        paths = [f['path'] for f in index['files']]
        if len(paths) != len(set(paths)) or set(paths) != set(expected):
            raise RuntimeError('Release downloads differ from current metadata')
        cache = root / 'dist/verified-downloads'
        cache.mkdir(parents=True, exist_ok=True)
        def verify_download(f):
            download = expected[f['path']]
            if f['downloads'] != [download['url']]:
                raise RuntimeError('Wrong download URL in release: ' + f['path'])
            path = cache / f['hashes']['sha512']
            if payload_root and (payload_root / f['path']).is_file():
                path = payload_root / f['path']
            if public or not path.exists():
                data = fetch(download['url'])
            else:
                data = path.read_bytes()
            for algo, digest in f['hashes'].items():
                if hashlib.new(algo, data).hexdigest() != digest:
                    raise RuntimeError('Artifact payload hash mismatch: ' + f['path'])
            if hashlib.new(download['hash-format'], data).hexdigest() != download['hash']:
                raise RuntimeError('Stale JAR/resource hash in release: ' + f['path'])
            if not path.exists():
                path.write_bytes(data)
            if f['path'].startswith('mods/'):
                import io
                with zipfile.ZipFile(io.BytesIO(data)) as jar:
                    if 'META-INF/mods.toml' in jar.namelist():
                        mods = tomllib.loads(jar.read('META-INF/mods.toml').decode())
                        return [(mod['modId'], f['path']) for mod in mods.get('mods', [])]
            return []
        with ThreadPoolExecutor(max_workers=6) as pool:
            found = list(pool.map(verify_download, index['files']))
        mod_ids = {}
        for mod, path in (entry for group in found for entry in group):
            if mod in mod_ids:
                raise RuntimeError('Duplicate mod ID in release downloads: ' + mod)
            mod_ids[mod] = path
        if any(n.endswith('.jar') and '/mods/' in n for n in names):
            raise RuntimeError('Unmanaged JAR embedded in overrides')
        defaults = (root / 'client-defaults/options.txt').read_bytes()
        if z.read('client-overrides/options.txt') != defaults:
            raise RuntimeError('Client options preset missing or stale')
        if 'overrides/options.txt' in names:
            raise RuntimeError('Options must be client-only')
        for path in ('gtl-update.py', 'update-gtl.sh', 'update-gtl.bat', 'gtl-known-jars.json'):
            if z.read('overrides/' + path) != (root / path).read_bytes():
                raise RuntimeError('Updater missing/stale: ' + path)
        resources = json.loads(next(line.split(':', 1)[1] for line in
                                   defaults.decode().splitlines() if line.startswith('resourcePacks:')))
        for resource in resources:
            if resource.startswith('file/') and 'resourcepacks/' + resource[5:] not in expected:
                raise RuntimeError('Preset references unpublished resource pack: ' + resource)
    if public:
        # Pages can lag git push: every required published byte must match this checkout.
        base = 'https://kairan0.github.io/gregtech-leisure-pack/'
        index_data = tomllib.loads((root / 'index.toml').read_text())
        targets = ['pack.toml', 'index.toml'] + [e['file'] for e in index_data['files']]
        def compare(path):
            from urllib.parse import quote
            actual = fetch(base + quote(path))
            if actual != (root / path).read_bytes():
                raise RuntimeError('Public Pages differs from release source: ' + path)
        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(compare, targets))
    print('Release verified:', archive.name, '-', len(expected), 'locked downloads')


def bundle(root, archive):
    # The live options.txt stays outside packwiz. Only first-time mrpack import gets it.
    with zipfile.ZipFile(archive, 'a', compression=zipfile.ZIP_DEFLATED) as z:
        if 'client-overrides/options.txt' in z.namelist():
            raise RuntimeError('Archive already finalized')
        index = json.loads(z.read('modrinth.index.json'))
        original = [{'path': f['path'], 'hashes': f['hashes']} for f in index['files']
                    if f['path'].startswith('mods/')]
        z.writestr('client-overrides/options.txt', (root / 'client-defaults/options.txt').read_bytes())
        z.writestr('overrides/gtl-import-jars.json', json.dumps(original, indent=2))


def payload_manifest(archive):
    result = {}
    with zipfile.ZipFile(archive) as z:
        if len(z.namelist()) != len(set(z.namelist())):
            raise RuntimeError('Duplicate ZIP entries in accepted artifact comparison')
        for name in z.namelist():
            if name.endswith('/'):
                continue
            data = z.read(name)
            # Export order is nondeterministic; only these generated sets are unordered.
            if name == 'modrinth.index.json':
                parsed = json.loads(data)
                parsed['files'].sort(key=lambda f: f['path'])
                data = json.dumps(parsed, sort_keys=True).encode()
            elif name == 'overrides/gtl-import-jars.json':
                data = json.dumps(sorted(json.loads(data), key=lambda f: f['path']), sort_keys=True).encode()
            result[name] = hashlib.sha256(data).hexdigest()
    return result


def compare_accepted(archive, accepted):
    current, previous = payload_manifest(archive), payload_manifest(accepted)
    changed = sorted(k for k in current.keys() | previous.keys() if current.get(k) != previous.get(k))
    if changed:
        raise RuntimeError('Payload differs from accepted candidate: ' + ', '.join(changed))
    print('Accepted candidate payload matches exactly (ignoring ZIP metadata and generated set order).')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--bundle', action='store_true')
    parser.add_argument('--public', action='store_true')
    parser.add_argument('--payload-root', type=Path, help='Optional hash-verified local download cache')
    parser.add_argument('--accepted-artifact', type=Path, help='Candidate already accepted in game')
    args = parser.parse_args()
    try:
        if args.bundle:
            bundle(args.root, args.archive)
        check(args.root, args.archive, args.public, args.payload_root)
        if args.accepted_artifact:
            compare_accepted(args.archive, args.accepted_artifact)
    except Exception as exc:
        print('RELEASE CHECK FAILED:', exc, file=sys.stderr)
        sys.exit(1)
