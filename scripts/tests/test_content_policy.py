import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

spec = importlib.util.spec_from_file_location('content_policy', Path(__file__).parents[1] / 'content_policy.py')
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


class ContentPolicyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def git(self, *args):
        return subprocess.run(['git', *args], cwd=self.root, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_ignored_legacy_tracked_data_still_blocks(self):
        self.git('init')
        data = self.root / 'gtcalcboard/personal_board.nbt'
        data.parent.mkdir()
        data.write_bytes(b'private fixture')
        (self.root / '.gitignore').write_text('/gtcalcboard/\n')
        self.git('add', '-f', 'gtcalcboard/personal_board.nbt')
        self.git('-c', 'user.name=Test', '-c', 'user.email=test@example.invalid',
                 'commit', '-m', 'Legacy data fixture')
        with self.assertRaisesRegex(RuntimeError, 'Unapproved repository path'):
            policy.check_repository(self.root)
        self.git('rm', '--cached', '--', 'gtcalcboard/personal_board.nbt')
        policy.check_repository(self.root)
        self.assertEqual(data.read_bytes(), b'private fixture')

    def test_repo_and_pack_have_separate_admission(self):
        for path in ('AGENTS.md', 'docs/ae2lt-gtceu-kubejs.md', 'scripts/test.py'):
            policy.require_path(path, 'repository')
            with self.assertRaises(RuntimeError):
                policy.require_path(path, 'pack')
        for path in ('config/gtcalcboard-client.toml', 'mods/gregtech-calculator-board.pw.toml',
                     'kubejs/data/recipe.json', 'config/skyblockbuilder/templates/default.nbt',
                     'resourcepacks/GTCalcBoard-zh_cn/assets/gtcalcboard/lang/zh_cn.json',
                     'client-defaults/options.txt'):
            policy.require_path(path, 'repository')
            policy.require_path(path, 'pack')

    def test_local_or_unreviewed_paths_blocked(self):
        for path in ('gtcalcboard/calcboard_save.nbt', 'gtcalcboard/client_preferences.json',
                     'gtcalcboard/servers/example.invalid/personal_board.nbt',
                     'docs/release-install-20260922.md', 'docs/another-investigation.md',
                     '.codex-trace/session.json', 'saves/test/level.dat', 'options.txt',
                     'config/.codexm/session.json', '../config/a', 'config/../gtcalcboard/a',
                     '/config/a', 'config\\a'):
            for audience in ('repository', 'pack'):
                with self.subTest(path=path, audience=audience), self.assertRaises(RuntimeError):
                    policy.require_path(path, audience)

    def test_index_rejects_personal_data(self):
        (self.root / 'index.toml').write_text('[[files]]\nfile="gtcalcboard/calcboard_save.nbt"\n')
        with self.assertRaisesRegex(RuntimeError, 'Unapproved pack path'):
            policy.check_index(self.root)

    def test_staged_index_cannot_be_hidden_by_working_copy(self):
        self.git('init')
        index = self.root / 'index.toml'
        index.write_text('[[files]]\nfile="gtcalcboard/calcboard_save.nbt"\n')
        self.git('add', 'index.toml')
        index.write_text('files=[]\n')
        policy.check_index(self.root)
        with self.assertRaisesRegex(RuntimeError, 'Unapproved pack path'):
            policy.check_index(self.root, staged=True)

    def test_archive_rejects_data_in_any_override_or_download(self):
        for name in ('overrides/gtcalcboard/save.nbt', 'client-overrides/gtcalcboard/save.nbt',
                     'server-overrides/gtcalcboard/save.nbt', 'overrides/docs/investigation.md',
                     'overrides/gtcalcboard/', 'gtcalcboard/save.nbt'):
            archive = self.root / 'test.mrpack'
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('modrinth.index.json', json.dumps({'files': []}))
                z.writestr(name, b'private fixture')
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                policy.check_archive(archive)
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('modrinth.index.json', json.dumps({'files': [{'path': 'gtcalcboard/save.nbt'}]}))
        with self.assertRaises(RuntimeError):
            policy.check_archive(archive)

    def test_valid_archive_keeps_explicit_options_seed(self):
        archive = self.root / 'test.mrpack'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('modrinth.index.json', json.dumps({'files': [{'path': 'mods/example.jar'}]}))
            z.writestr('client-overrides/options.txt', 'lang:zh_cn')
            z.writestr('overrides/gtl-import-jars.json', '[]')
        policy.check_archive(archive)

    def test_export_and_publish_stop_before_external_commands(self):
        self.git('init')
        scripts = self.root / 'scripts'
        scripts.mkdir()
        for name in ('content_policy.py', 'export-mrpack.sh', 'publish.sh'):
            shutil.copy2(Path(__file__).parents[1] / name, scripts / name)
        (self.root / 'pack.toml').write_text('version="test"\n')
        (self.root / 'index.toml').write_text('files=[]\n')
        data = self.root / 'gtcalcboard/save.nbt'
        data.parent.mkdir()
        data.write_bytes(b'private fixture')
        self.git('add', 'gtcalcboard/save.nbt', 'pack.toml', 'index.toml')
        archive = self.root / 'accepted.mrpack'
        with zipfile.ZipFile(archive, 'w') as z:
            z.writestr('modrinth.index.json', '{"files": []}')
        # These scripts would hit missing packwiz/gh next; require the content
        # rejection itself, including preview and resume entry points.
        for command in (
            ['bash', 'scripts/export-mrpack.sh', '--preview'],
            ['bash', 'scripts/publish.sh', '--accepted-artifact', str(archive)],
            ['bash', 'scripts/publish.sh', '--accepted-artifact', str(archive), '--resume-checked-build'],
        ):
            result = subprocess.run(command, cwd=self.root, capture_output=True, text=True,
                                    env={**os.environ, 'GTL_PYTHON': sys.executable})
            with self.subTest(command=command):
                self.assertEqual(result.returncode, 1)
                self.assertIn('CONTENT CHECK FAILED: Unapproved repository path: gtcalcboard/save.nbt', result.stderr)


if __name__ == '__main__':
    unittest.main()
