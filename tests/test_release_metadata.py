import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("release_metadata", Path(__file__).resolve().parents[1] / "script/release_metadata.py")
metadata = importlib.util.module_from_spec(spec)
spec.loader.exec_module(metadata)


class ReleaseMetadataTests(unittest.TestCase):
    def test_tag_uses_triggering_ref(self):
        result = metadata.build_metadata("push", "refs/tags/v1.2.3", "1234567890abcdef")
        self.assertEqual(result, {"PACKAGE_PREFIX": "bika_v1.2.3", "TAG_NAME": "v1.2.3", "HEAD_SHA_SHORT": "1234567"})

    def test_manual_build_is_development_even_on_tag(self):
        for ref in ("refs/heads/main", "refs/tags/v1.2.3"):
            result = metadata.build_metadata("workflow_dispatch", ref, "abcdef1234567890")
            self.assertEqual(result["PACKAGE_PREFIX"], "bika_dev_abcdef1")
            self.assertEqual(result["TAG_NAME"], "")

    def test_branch_push_is_not_a_release(self):
        self.assertEqual(metadata.build_metadata("push", "refs/heads/main", "123456789")["TAG_NAME"], "")

    def test_writes_github_output_without_replacing_existing_values(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            output.write_text("EXISTING=value\n", encoding="utf-8")
            with patch.dict(os.environ, GITHUB_EVENT_NAME="workflow_dispatch", GITHUB_REF="refs/heads/main", GITHUB_SHA="abcdef1234", GITHUB_OUTPUT=str(output)):
                metadata.main()
            self.assertEqual(output.read_text(encoding="utf-8"), "EXISTING=value\nPACKAGE_PREFIX=bika_dev_abcdef1\nTAG_NAME=\nHEAD_SHA_SHORT=abcdef1\n")


if __name__ == "__main__":
    unittest.main()
