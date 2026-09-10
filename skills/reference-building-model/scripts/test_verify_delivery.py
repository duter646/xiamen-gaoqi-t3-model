import json
import tempfile
import unittest
from pathlib import Path

from verify_delivery import sha256, validate


class DeliveryEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.model = self.root / 'model.glb'
        self.model.write_bytes(b'fixture: not a geometry validation')
        self.evidence = self.root / 'check.json'
        self.evidence.write_text('{"result": "fixture"}', encoding='utf-8')
        model_hash = sha256(self.model)
        self.data = {
            'artifacts': {'model': {'path': 'model.glb', 'sha256': model_hash}},
            'required_checks': ['geometry'],
            'checks': [{'id': 'geometry', 'status': 'pass', 'scope': 'fixture only',
                        'artifacts': {'model': model_hash},
                        'evidence': [{'path': 'check.json', 'sha256': sha256(self.evidence)}]}]
        }

    def result(self):
        manifest = self.root / 'delivery.json'
        manifest.write_text(json.dumps(self.data), encoding='utf-8')
        return validate(manifest)

    def test_matching_evidence(self):
        self.assertTrue(self.result()['passed'])

    def test_changed_model_requires_new_check_even_if_manifest_hash_updated(self):
        self.model.write_bytes(b'changed model')
        self.data['artifacts']['model']['sha256'] = sha256(self.model)
        self.assertFalse(self.result()['passed'])

    def test_changed_evidence(self):
        self.evidence.write_text('different report', encoding='utf-8')
        self.assertFalse(self.result()['passed'])

    def test_missing_check(self):
        self.data['required_checks'].append('circulation')
        self.assertFalse(self.result()['passed'])

    def test_failed_check(self):
        self.data['checks'][0]['status'] = 'fail'
        self.assertFalse(self.result()['passed'])

    def test_path_outside_manifest(self):
        self.data['checks'][0]['evidence'][0]['path'] = '../outside.json'
        self.assertFalse(self.result()['passed'])


if __name__ == '__main__':
    unittest.main()
