import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

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


if __name__ == '__main__':
    unittest.main()
