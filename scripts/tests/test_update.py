import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
import hashlib
import io
from unittest.mock import patch
import subprocess

MODULE = Path(__file__).resolve().parents[2] / 'gtl-update.py'
spec = importlib.util.spec_from_file_location('update', MODULE)
update = importlib.util.module_from_spec(spec)
spec.loader.exec_module(update)


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'mods').mkdir()

    def jar(self, name, mod='ae2lt', payload='old'):
        path = self.root / 'mods' / name
        with zipfile.ZipFile(path, 'w') as z:
            z.writestr('META-INF/mods.toml', '[[mods]]\nmodId="%s"\nversion="2.1.0-beta.3"\n' % mod)
            z.writestr('payload', payload)
        return {'path': 'mods/' + name,
                'hashes': {'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}}

    def state(self, record):
        return {'cachedSide': 'client', 'packFileHash': {'type': 'sha256', 'value': 'a'},
                'indexFileHash': {'type': 'sha256', 'value': 'b'},
                'cachedFiles': {'mods/lt.pw.toml': {
                    'cachedLocation': record['path'], 'optionValue': True,
                    'linkedFileHash': {'type': 'sha256', 'value': record['hashes']['sha256']}}}}

    def test_import_without_packwiz_history_retires_only_verified_original(self):
        old = self.jar('old.jar')
        new = self.jar('new.jar', payload='new')
        addon = self.jar('addon.jar', mod='addon')
        update.finalize(self.root, self.state(new), [old])
        self.assertFalse((self.root / old['path']).exists())
        self.assertTrue((self.root / new['path']).exists())
        self.assertTrue((self.root / addon['path']).exists())
        self.assertEqual(len(list((self.root / 'backups').rglob('old.jar'))), 1)

    def test_modified_duplicate_blocks_without_moving_anything(self):
        old = self.jar('old.jar')
        new = self.jar('new.jar', payload='new')
        self.jar('old.jar', payload='player-modified')
        with self.assertRaisesRegex(RuntimeError, 'Unrecognized'):
            update.finalize(self.root, self.state(new), [old])
        self.assertTrue((self.root / old['path']).exists())

    def test_corrupt_current_blocks_retirement(self):
        old = self.jar('old.jar')
        new = self.jar('new.jar', payload='new')
        self.jar('new.jar', payload='corrupt')
        with self.assertRaisesRegex(RuntimeError, 'hash'):
            update.finalize(self.root, self.state(new), [old])
        self.assertTrue((self.root / old['path']).exists())

    def test_existing_target_with_previous_packwiz_state(self):
        old = self.jar('old.jar')
        new = self.jar('new.jar', payload='new')
        previous = update.records(self.state(old))
        update.finalize(self.root, self.state(new), previous)
        update.finalize(self.root, self.state(new), previous)  # repeat is safe
        self.assertFalse((self.root / old['path']).exists())

    def test_unknown_duplicate_blocks_even_without_history(self):
        self.jar('unknown.jar')
        new = self.jar('new.jar', payload='new')
        with self.assertRaisesRegex(RuntimeError, 'Unrecognized'):
            update.finalize(self.root, self.state(new), [])

    def test_preserves_player_options_and_seeds_only_missing(self):
        (self.root / 'client-defaults').mkdir()
        (self.root / 'client-defaults/options.txt').write_text('lang:zh_cn\n')
        update.seed_options(self.root)
        self.assertEqual((self.root / 'options.txt').read_text(), 'lang:zh_cn\n')
        (self.root / 'options.txt').write_text('lang:en_us\n')
        update.seed_options(self.root)
        self.assertEqual((self.root / 'options.txt').read_text(), 'lang:en_us\n')

    def test_path_escape_rejected(self):
        with self.assertRaises(RuntimeError):
            update.safe_path(self.root, '../outside.jar')
        (self.root / 'mods/link').symlink_to(self.root.parent, target_is_directory=True)
        with self.assertRaises(RuntimeError):
            update.safe_path(self.root, 'mods/link/outside.jar')

    def test_failed_upstream_restores_deleted_old_jar_and_never_succeeds(self):
        old = self.jar('old.jar')
        (self.root / 'packwiz.json').write_text(json.dumps(self.state(old)))
        boot = b'fixture-bootstrap'
        (self.root / 'packwiz-installer-bootstrap.jar').write_bytes(boot)
        pack = b'[index]\nhash-format="sha256"\nhash="b"\n'
        def fail(*args, **kwargs):
            (self.root / old['path']).unlink()  # Simulate upstream partial rename.
            raise subprocess.CalledProcessError(1, ['fixture-installer'])
        with patch.object(update, 'BOOT_SHA', hashlib.sha256(boot).hexdigest()), \
                patch.object(update.urllib.request, 'urlopen', return_value=io.BytesIO(pack)), \
                patch.object(update.subprocess, 'run', side_effect=fail):
            with self.assertRaises(subprocess.CalledProcessError):
                update.update(self.root, 'java', 'client', 'https://example.test/pack.toml')
        self.assertTrue((self.root / old['path']).exists())
        self.assertFalse((self.root / '.gtl-update-lock').exists())
        self.assertIn(old, json.loads((self.root / '.gtl-update-history.json').read_text()))

    def test_disabled_jar_is_untouched(self):
        old = self.jar('old.jar')
        (self.root / old['path']).rename(self.root / 'mods/old.jar.disabled')
        new = self.jar('new.jar', payload='new')
        update.finalize(self.root, self.state(new), [old])
        self.assertTrue((self.root / 'mods/old.jar.disabled').exists())

    def test_two_unknown_addons_with_same_id_block(self):
        self.jar('a.jar', mod='addon')
        self.jar('b.jar', mod='addon')
        new = self.jar('new.jar', payload='new')
        with self.assertRaisesRegex(RuntimeError, 'duplicate mod ID'):
            update.finalize(self.root, self.state(new), [])

    def test_modified_tracked_old_jar_blocks_before_upstream_can_delete_it(self):
        old = self.jar('old.jar')
        (self.root / 'packwiz.json').write_text(json.dumps(self.state(old)))
        self.jar('old.jar', payload='my-custom-build')
        with patch.object(update.subprocess, 'run') as java:
            with self.assertRaisesRegex(RuntimeError, 'modified managed JAR'):
                update.update(self.root, 'java', 'client', 'https://example.test/pack.toml')
            java.assert_not_called()
        self.assertTrue((self.root / old['path']).exists())

    def test_managed_directory_symlink_blocks_before_java(self):
        (self.root / 'client-defaults').symlink_to(self.root.parent, target_is_directory=True)
        with patch.object(update.subprocess, 'run') as java:
            with self.assertRaisesRegex(RuntimeError, 'escapes|Symlink'):
                update.update(self.root, 'java', 'client', 'https://example.test/pack.toml')
            java.assert_not_called()

    def test_keyboard_interrupt_restores_old_jar(self):
        self.failure_after_java(KeyboardInterrupt(), options_failure=False)

    def test_options_failure_restores_archived_old_jar(self):
        self.failure_after_java(OSError('disk full'), options_failure=True)

    def failure_after_java(self, error, options_failure):
        old = self.jar('old.jar')
        new = self.jar('new.jar', payload='new')
        (self.root / 'packwiz.json').write_text(json.dumps(self.state(old)))
        boot = b'fixture-bootstrap'
        (self.root / 'packwiz-installer-bootstrap.jar').write_bytes(boot)
        pack = b'[index]\nhash-format="sha256"\nhash="b"\n'
        def install(*args, **kwargs):
            if not options_failure:
                (self.root / old['path']).unlink()
                raise error
            state = self.state(new)
            state['packFileHash']['value'] = hashlib.sha256(pack).hexdigest()
            (self.root / 'packwiz.json').write_text(json.dumps(state))
        with patch.object(update, 'BOOT_SHA', hashlib.sha256(boot).hexdigest()), \
                patch.object(update.urllib.request, 'urlopen', return_value=io.BytesIO(pack)), \
                patch.object(update.subprocess, 'run', side_effect=install), \
                patch.object(update, 'seed_options', side_effect=error):
            with self.assertRaises(type(error)):
                update.update(self.root, 'java', 'client', 'https://example.test/pack.toml')
        self.assertTrue((self.root / old['path']).exists())
        self.assertFalse((self.root / '.gtl-update-lock').exists())


if __name__ == '__main__':
    unittest.main()
