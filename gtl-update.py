#!/usr/bin/env python3
"""Verified packwiz update with recoverable JAR retirement. Requires Python 3.11+."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import tomllib
import urllib.request
import zipfile

PACK_URL = 'https://kairan0.github.io/gregtech-leisure-pack/pack.toml'
BOOT_URL = 'https://github.com/packwiz/packwiz-installer-bootstrap/releases/download/v0.0.3/packwiz-installer-bootstrap.jar'
BOOT_SHA = 'a8fbb24dc604278e97f4688e82d3d91a318b98efc08d5dbfcbcbcab6443d116c'


def safe_path(root, relative):
    rel = PurePosixPath(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in relative or ':' in relative:
        raise RuntimeError('Unsafe path: ' + relative)
    path = root / rel
    if not path.resolve().is_relative_to(root.resolve()):
        raise RuntimeError('Path escapes instance: ' + relative)
    # Avoid manipulating a symlink even when its current destination is inside.
    if any(p.is_symlink() for p in [path, *path.parents] if p.is_relative_to(root)):
        raise RuntimeError('Symlink is not a managed file: ' + relative)
    return path


def matches(path, hashes):
    if not path.is_file() or not hashes:
        return False
    data = path.read_bytes()
    return all(algorithm in ('sha256', 'sha512', 'sha1') and
               hashlib.new(algorithm, data).hexdigest() == digest
               for algorithm, digest in hashes.items())


def records(state):
    result = []
    for entry in state.get('cachedFiles', {}).values():
        location = entry.get('cachedLocation')
        if (not location or not location.startswith('mods/') or not location.endswith('.jar')
                or entry.get('onlyOtherSide') or
                (entry.get('isOptional') and not entry.get('optionValue'))):
            continue
        digest = entry.get('linkedFileHash', entry.get('hash'))
        if not digest:
            raise RuntimeError('No expected hash for ' + location)
        result.append({'path': location, 'hashes': {digest['type']: digest['value']}})
    return result


def mod_ids(path):
    with zipfile.ZipFile(path) as jar:
        if 'META-INF/mods.toml' not in jar.namelist():
            return set()  # Library JAR: hash checked, not an independent Forge mod.
        data = tomllib.loads(jar.read('META-INF/mods.toml').decode('utf-8'))
    return {mod['modId'] for mod in data.get('mods', [])}


def finalize(root, state, known):
    if not state.get('packFileHash') or not state.get('indexFileHash'):
        raise RuntimeError('packwiz did not complete the manifest update')
    current = records(state)
    if not current:
        raise RuntimeError('No canonical mods in packwiz state')
    canonical = {}
    ids = {}
    for entry in current:
        path = safe_path(root, entry['path'])
        if not matches(path, entry['hashes']):
            raise RuntimeError('Canonical JAR hash mismatch: ' + entry['path'])
        canonical[path] = mod_ids(path)
        for mod in canonical[path]:
            if mod in ids:
                raise RuntimeError('Published manifest contains duplicate mod ID: ' + mod)
            ids[mod] = path
    obsolete = []
    all_ids = {}
    for path in sorted((root / 'mods').glob('*.jar')):
        safe_path(root, path.relative_to(root).as_posix())
        found = mod_ids(path)
        if path not in canonical and found.intersection(ids):
            if not found.issubset(ids):
                raise RuntimeError('Unrecognized mixed-mod duplicate: ' + path.name)
            if not any(entry['path'] == path.relative_to(root).as_posix() and
                       matches(path, entry['hashes']) for entry in known):
                raise RuntimeError('Unrecognized/modified duplicate; preserved: ' + path.name)
            obsolete.append(path)
        else:
            for mod in found:
                if mod in all_ids:
                    raise RuntimeError('Unrecognized duplicate mod ID: ' + mod)
                all_ids[mod] = path
    # Plan and validate everything before moving any file.
    if obsolete:
        backup_root = safe_path(root, 'backups')
        backup_root.mkdir(exist_ok=True)
        backup = Path(tempfile.mkdtemp(prefix='superseded-jars-', dir=backup_root))
        for path in obsolete:
            shutil.move(str(path), backup / path.name)
        print('Archived superseded JARs:', ', '.join(p.name for p in obsolete))
    print('Verified', len(current), 'canonical JARs; no duplicate mod IDs.')


def seed_options(root):
    source = safe_path(root, 'client-defaults/options.txt')
    target = safe_path(root, 'options.txt')
    if source.is_file() and not target.exists():
        with target.open('xb') as output:
            output.write(source.read_bytes())


def read_state(root):
    path = safe_path(root, 'packwiz.json')
    return json.loads(path.read_text()) if path.exists() else {}


def preflight_links(root):
    # Upstream writes through parent directory symlinks. Check managed trees before
    # invoking it, including first imports without any packwiz state yet.
    for name in ('mods', 'config', 'defaultconfigs', 'client-defaults', 'kubejs',
                 'ldlib', 'packmenu', 'patchouli_books', 'resourcepacks', 'shaderpacks',
                 'skyblockbuilder', 'gtcalcboard'):
        base = safe_path(root, name)
        if base.is_dir():
            for path in base.rglob('*'):
                if path.is_symlink():
                    raise RuntimeError('Symlink in managed tree; preserved: ' + str(path))


def update(root, java, side, pack_url):
    root = root.resolve()
    lock = safe_path(root, '.gtl-update-lock')
    lock.mkdir()  # Exclusive, fail closed on a concurrent/interrupted invocation.
    try:
        preflight_links(root)
        old_state = read_state(root)
        known = records(old_state)
        for relative in ('gtl-known-jars.json', 'gtl-import-jars.json', '.gtl-update-history.json'):
            path = safe_path(root, relative)
            if path.exists():
                known += json.loads(path.read_text())
        # Retain old records across partial upstream updates and retries.
        known = list({json.dumps(entry, sort_keys=True): entry for entry in known}.values())
        by_path = {}
        for entry in known:
            by_path.setdefault(entry['path'], []).append(entry['hashes'])
        # Upstream can delete renamed tracked files itself. Protect modified originals
        # BEFORE invoking it, not merely in the post-update duplicate check.
        for relative, hashes in by_path.items():
            path = safe_path(root, relative)
            if path.exists() and not any(matches(path, expected) for expected in hashes):
                raise RuntimeError('Unrecognized/modified managed JAR; preserved: ' + relative)
        history = safe_path(root, '.gtl-update-history.json')
        history_tmp = safe_path(root, '.gtl-update-history.json.tmp')
        history_tmp.write_text(json.dumps(known, indent=2))
        history_tmp.replace(history)
        backups = safe_path(root, 'backups')
        backups.mkdir(exist_ok=True)
        snapshot = Path(tempfile.mkdtemp(prefix='pre-update-', dir=backups))
        objects = safe_path(root, 'backups/verified-jar-objects')
        objects.mkdir(exist_ok=True)
        (snapshot / 'packwiz.json').write_text(json.dumps(old_state, indent=2))
        # Retain verified originals before upstream can delete a renamed tracked file.
        for entry in known:
            path = safe_path(root, entry['path'])
            target = snapshot / path.name
            if matches(path, entry['hashes']) and not target.exists():
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                saved = objects / digest
                if not matches(saved, {'sha256': digest}):
                    shutil.copy2(path, saved)
                # Link only immutable backup objects, NEVER live mod files.
                try:
                    os.link(saved, target)
                except OSError:
                    shutil.copy2(saved, target)
        bootstrap = safe_path(root, 'packwiz-installer-bootstrap.jar')
        if not matches(bootstrap, {'sha256': BOOT_SHA}):
            with urllib.request.urlopen(BOOT_URL, timeout=120) as response:
                data = response.read()
            if hashlib.sha256(data).hexdigest() != BOOT_SHA:
                raise RuntimeError('Bootstrap hash mismatch')
            bootstrap.write_bytes(data)
        # Freeze expected manifest bytes; fail if Pages changes during installation.
        with urllib.request.urlopen(pack_url, timeout=60) as response:
            pack_bytes = response.read()
        expected_pack = hashlib.sha256(pack_bytes).hexdigest()
        expected_index = tomllib.loads(pack_bytes.decode())['index']
        try:
            subprocess.run([java, '-jar', str(bootstrap), '-g', '-s', side, pack_url],
                           cwd=root, check=True)
            state = read_state(root)
            if state.get('cachedSide') != side or state.get('packFileHash') != {
                    'type': 'sha256', 'value': expected_pack}:
                raise RuntimeError('Installed manifest differs from the requested release; retry')
            if state.get('indexFileHash') != {'type': expected_index['hash-format'],
                                               'value': expected_index['hash']}:
                raise RuntimeError('Installed index differs from the requested release; retry')
            finalize(root, state, known)
            if side == 'client':
                seed_options(root)
        except BaseException:
            # Restore missing old tracked files on failure; never overwrite a changed file.
            for entry in known:
                path = safe_path(root, entry['path'])
                saved = snapshot / path.name
                if not path.exists() and matches(saved, entry['hashes']):
                    path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(saved, path)
            raise
        print('Update verified successfully. Snapshot:', snapshot)
    finally:
        lock.rmdir()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--java', default='java')
    parser.add_argument('--side', choices=['client', 'server'], default='client')
    parser.add_argument('--pack-url', default=PACK_URL)
    args = parser.parse_args()
    try:
        update(args.root, args.java, args.side, args.pack_url)
    except Exception as exc:
        print('UPDATE FAILED; do not start Minecraft:', exc, file=sys.stderr)
        sys.exit(1)
