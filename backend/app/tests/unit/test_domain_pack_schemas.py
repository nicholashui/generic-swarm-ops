"""Wave 0 Domain Pack schema validation (stdlib validator)."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "scripts" / "business"
sys.path.insert(0, str(SCRIPTS))

from schema_validate import SchemaError, validate  # noqa: E402


class DomainPackSchemaTests(unittest.TestCase):
    def _load(self, *parts: str) -> dict:
        return json.loads((ROOT.joinpath(*parts)).read_text(encoding="utf-8"))

    def test_positive_domain_manifest(self):
        schema = self._load("business", "schemas", "domain-manifest.schema.json")
        data = self._load("business", "fixtures", "positive", "domain-manifest.video.example.json")
        validate(data, schema)

    def test_negative_domain_manifest(self):
        schema = self._load("business", "schemas", "domain-manifest.schema.json")
        data = self._load("business", "fixtures", "negative", "domain-manifest.invalid.json")
        with self.assertRaises(SchemaError):
            validate(data, schema)

    def test_positive_agent_spec(self):
        schema = self._load("business", "schemas", "agent-spec.schema.json")
        data = self._load("business", "fixtures", "positive", "agent-spec.video.example.json")
        validate(data, schema)

    def test_negative_agent_spec(self):
        schema = self._load("business", "schemas", "agent-spec.schema.json")
        data = self._load("business", "fixtures", "negative", "agent-spec.missing-alc.json")
        with self.assertRaises(SchemaError):
            validate(data, schema)

    def test_positive_learning_log(self):
        schema = self._load("business", "schemas", "learning-log.schema.json")
        data = self._load("business", "fixtures", "positive", "learning-log.example.json")
        validate(data, schema)

    def test_video_manifest_file_validates(self):
        schema = self._load("business", "schemas", "domain-manifest.schema.json")
        path = ROOT / "business" / "video" / "manifest.json"
        self.assertTrue(path.is_file())
        validate(self._load("business", "video", "manifest.json"), schema)


if __name__ == "__main__":
    unittest.main()
