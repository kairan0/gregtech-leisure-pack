#!/usr/bin/env python3
"""Path admission checks; content suitability still requires human review."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tomllib
import zipfile


GAME_TREES = {'config', 'defaultconfigs', 'kubejs', 'mods', 'packmenu',
              'resourcepacks', 'shaderpacks'}
GAME_FILES = {'log4j2.xml', 'gtl-update.py', 'gtl-known-jars.json',
              'update-gtl.sh', 'update-gtl.bat', 'client-defaults/options.txt'}
REPO_FILES = GAME_FILES | {
    '.gitattributes', '.gitignore', '.packwizignore', '.nojekyll',
    'AGENTS.md', 'README.md', 'CHANGELOG.md', 'CODEX_INSTALL.md',
    'pack.toml', 'index.toml', 'docs/ae2lt-gtceu-kubejs.md',
    '.agents/skills/gtl-release/SKILL.md',
    '.agents/skills/gtl-release/references/acceptance.md',
    '.agents/skills/gtl-release/agents/openai.yaml',
}
LOCAL_COMPONENTS = {'.git', '.codex', '.codexm', '.codex-trace', '__pycache__'}


def parts(path):
    values = path.split('/')
    if (not path or '\\' in path or any(p in ('', '.', '..') for p in values)
            or any(ord(c) < 32 for c in path)):
        raise RuntimeError('Unsafe content path: ' + repr(path))
    if any(p in LOCAL_COMPONENTS for p in values):
        raise RuntimeError('Local state in public content: ' + path)
    return values


def require_path(path, audience):
    values = parts(path)
    allowed = path in (REPO_FILES if audience == 'repository' else GAME_FILES)
    if len(values) > 1 and values[0] in GAME_TREES:
        allowed = True
    if audience == 'repository' and len(values) > 1 and values[0] in ('scripts', '.github'):
        allowed = True
    if not allowed:
        raise RuntimeError('Unapproved ' + audience + ' path: ' + path)


def check_repository(root):
    # Inspect the whole staged tree, including unchanged legacy files. Ignore rules
    # never authorize a file that is already tracked or was force-added.
    listing = subprocess.check_output(['git', 'ls-files', '--stage', '-z'], cwd=root)
    records = [record for record in listing.split(b'\0') if record]
    for record in records:
        info, raw = record.split(b'\t', 1)
        mode, _, stage = info.split()
        path = raw.decode('utf-8')
        if mode not in (b'100644', b'100755') or stage != b'0':
            raise RuntimeError('Unsupported staged entry: ' + path)
        require_path(path, 'repository')
    print('Repository content paths verified:', len(records))


def check_index(root, staged=False):
    text = (subprocess.check_output(['git', 'show', ':index.toml'], cwd=root).decode()
            if staged else (root / 'index.toml').read_text())
    data = tomllib.loads(text)
    for entry in data['files']:
        require_path(entry['file'], 'pack')
    print('Pack index content paths verified:', len(data['files']), '(staged)' if staged else '(working)')


def check_archive(archive):
    with zipfile.ZipFile(archive) as z:
        for entry in z.infolist():
            name = entry.filename
            if name == 'modrinth.index.json':
                continue
            values = parts(name.rstrip('/'))
            if values[0] not in ('overrides', 'client-overrides', 'server-overrides'):
                raise RuntimeError('Unapproved archive entry: ' + name)
            if len(values) == 1 and entry.is_dir():
                continue
            target = '/'.join(values[1:])
            # Directory markers do not carry content, but private roots must fail too.
            if entry.is_dir() and target in GAME_TREES | {'client-defaults'}:
                continue
            if name == 'client-overrides/options.txt' or name == 'overrides/gtl-import-jars.json':
                continue
            require_path(target, 'pack')
        index = json.loads(z.read('modrinth.index.json'))
        for entry in index['files']:
            require_path(entry['path'], 'pack')
    print('Archive content paths verified:', archive.name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--archive', type=Path)
    args = parser.parse_args()
    try:
        check_repository(args.root)
        check_index(args.root, staged=True)
        check_index(args.root)
        if args.archive:
            check_archive(args.archive)
    except (RuntimeError, OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print('CONTENT CHECK FAILED:', exc, file=sys.stderr)
        sys.exit(1)
