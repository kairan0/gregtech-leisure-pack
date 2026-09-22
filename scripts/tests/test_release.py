import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile
from unittest.mock import patch
import urllib.error
import io

spec = importlib.util.spec_from_file_location('release', Path(__file__).parents[1] / 'release-check.py')
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


class ReleaseTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'mods').mkdir()
        (self.root / 'client-defaults').mkdir()
        (self.root / 'client-defaults/options.txt').write_text('resourcePacks:["vanilla"]\n')
        (self.root / 'pack.toml').write_text('version="test"\n')
        for f in ('gtl-update.py', 'update-gtl.sh', 'update-gtl.bat', 'gtl-known-jars.json'):
            (self.root / f).write_text('fixture')
        self.files = []

    def jar(self, filename, mod):
        p = self.root / 'mods' / filename
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('META-INF/mods.toml', '[[mods]]\nmodId="%s"\n' % mod)
        data = p.read_bytes()
        (self.root / 'mods' / (filename + '.pw.toml')).write_text(
            'filename="%s"\n[download]\nurl="https://example.test/%s"\n'
            'hash-format="sha256"\nhash="%s"\n' % (filename, filename, hashlib.sha256(data).hexdigest()))
        self.files.append({'path': 'mods/' + filename, 'downloads': ['https://example.test/' + filename],
                           'hashes': {'sha512': hashlib.sha512(data).hexdigest()}})

    def archive(self):
        p = self.root / 'test.mrpack'
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr('modrinth.index.json', json.dumps({'versionId': 'test', 'files': self.files}))
            for f in ('gtl-update.py', 'update-gtl.sh', 'update-gtl.bat', 'gtl-known-jars.json'):
                z.write(self.root / f, 'overrides/' + f)
        release.bundle(self.root, p)
        return p

    def test_valid_fresh_pack(self):
        self.jar('new.jar', 'ae2lt')
        release.check(self.root, self.archive(), payload_root=self.root)

    def test_two_jars_for_one_mod_rejected(self):
        self.jar('old.jar', 'ae2lt')
        self.jar('new.jar', 'ae2lt')
        with self.assertRaisesRegex(RuntimeError, 'Duplicate mod ID'):
            release.check(self.root, self.archive(), payload_root=self.root)

    def test_old_release_cannot_pass_new_metadata_gate(self):
        self.jar('old.jar', 'ae2lt')
        archive = self.archive()
        (self.root / 'mods/old.jar.pw.toml').unlink()
        self.jar('new.jar', 'ae2lt')
        with self.assertRaisesRegex(RuntimeError, 'differ from current metadata'):
            release.check(self.root, archive, payload_root=self.root)

    def test_unpublished_resource_pack_in_options_blocks_release(self):
        self.jar('new.jar', 'ae2lt')
        (self.root / 'client-defaults/options.txt').write_text('resourcePacks:["file/missing.zip"]\n')
        with self.assertRaisesRegex(RuntimeError, 'unpublished resource pack'):
            release.check(self.root, self.archive(), payload_root=self.root)

    def test_changed_game_file_invalidates_gameplay_acceptance(self):
        self.jar('new.jar', 'ae2lt')
        accepted = self.archive()
        changed = self.root / 'changed.mrpack'
        with zipfile.ZipFile(accepted) as src, zipfile.ZipFile(changed, 'w') as out:
            for name in src.namelist():
                out.writestr(name, src.read(name))
            out.writestr('overrides/config/changed.toml', 'changed=true')
        with self.assertRaisesRegex(RuntimeError, 'Payload differs'):
            release.compare_accepted(changed, accepted)

    def test_zip_timestamp_and_generated_order_do_not_invalidate_acceptance(self):
        self.jar('a.jar', 'a')
        self.jar('b.jar', 'b')
        accepted = self.archive()
        rebuilt = self.root / 'rebuilt.mrpack'
        with zipfile.ZipFile(accepted) as src, zipfile.ZipFile(rebuilt, 'w') as out:
            for name in reversed(src.namelist()):
                data = src.read(name)
                if name == 'modrinth.index.json':
                    parsed = json.loads(data)
                    parsed['files'].reverse()
                    data = json.dumps(parsed)
                out.writestr(zipfile.ZipInfo(name, date_time=(2020,1,1,0,0,0)), data)
        release.compare_accepted(rebuilt, accepted)

    def test_transient_public_download_is_retried_without_cache_fallback(self):
        error = urllib.error.HTTPError('https://example.test', 503, 'unavailable', {}, None)
        with patch.object(release.urllib.request, 'urlopen', side_effect=[error, io.BytesIO(b'actual network')]) as get, \
                patch.object(release.time, 'sleep'):
            self.assertEqual(release.fetch('https://example.test'), b'actual network')
            self.assertEqual(get.call_count, 2)

    def test_public_download_retry_is_bounded(self):
        error = urllib.error.HTTPError('https://example.test', 503, 'unavailable', {}, None)
        with patch.object(release.urllib.request, 'urlopen', side_effect=error) as get, \
                patch.object(release.time, 'sleep'):
            with self.assertRaisesRegex(RuntimeError, 'after 3 attempts'):
                release.fetch('https://example.test')
            self.assertEqual(get.call_count, 3)


if __name__ == '__main__':
    unittest.main()
