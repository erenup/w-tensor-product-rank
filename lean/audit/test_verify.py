#!/usr/bin/env python3
"""Negative controls for source inspection, dependency output, and execution."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
import verify


VALID_OUTPUT = "".join("'" + name + "' depends on axioms: "
                       "[propext, Classical.choice, Quot.sound]\n"
                       for name in verify.AXIOM_THEOREMS)


class AuditControls(unittest.TestCase):
    def test_valid_sources_and_output(self):
        root = self.fixture()
        (root / "TR29" / "Blocks.lean").write_bytes(
            (verify.ROOT / "TR29" / "Blocks.lean").read_bytes())
        snapshot = verify.check_sources(root)
        self.assertIn("TR29/Blocks.lean", snapshot)
        self.assertEqual(set(verify.check_configuration(root)), set(verify.CONFIGURATION_HASHES))
        self.assertEqual(verify.parse_axioms(VALID_OUTPUT), verify.EXPECTED_AXIOMS)
        self.assertEqual(verify.parse_axioms(VALID_OUTPUT.replace(
            "propext, Classical.choice, Quot.sound", "Quot.sound, propext, Classical.choice")),
            verify.EXPECTED_AXIOMS)

    def test_forbidden_proof_tokens(self):
        for source in (
            "theorem bad : False := by sorry",
            "theorem bad : False := by\n  admit",
            "axiom bad : False", "axiom/- declaration -/bad : False",
            "theorem bad : False := by\n  «sorry»",
            "theorem bad : False := by\n  exact sorryAx _ false",
            "unsafe def bad := 0", "by native_decide",
            "@[implemented_by bad] def safe := 0", "Lean.ofReduceBool",
            '/- sorry -/', 'def text := "admit"',
        ):
            with self.subTest(source=source), self.assertRaises(verify.AuditError):
                verify.reject_forbidden(source, "example.lean")

    def test_missing_extra_and_malformed_axiom_output(self):
        for output in (
            "", "Build completed successfully.\n", VALID_OUTPUT + VALID_OUTPUT,
            "unrelated output\n" + VALID_OUTPUT, VALID_OUTPUT + "extra output\n",
            VALID_OUTPUT.replace("core_theorems", "otherTheorem"),
            VALID_OUTPUT.replace("]", ", sorryAx]"),
            VALID_OUTPUT.replace(", Quot.sound", ""),
            VALID_OUTPUT.replace("Quot.sound", "propext"),
            VALID_OUTPUT.replace("]", ", propext]"),
            VALID_OUTPUT.replace("[propext, Classical.choice, Quot.sound]", "[]"),
            VALID_OUTPUT.replace("]", ""),
        ):
            with self.subTest(output=output), self.assertRaises(verify.AuditError):
                verify.parse_axioms(output)
        with self.assertRaises(verify.AuditError):
            verify.parse_axioms(VALID_OUTPUT, "warning: unexpected diagnostic\n")

    def fixture(self):
        temporary_root = verify.ROOT / ".lake"
        temporary_root.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="audit-control-", dir=temporary_root)
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        names = (verify.REQUIRED_SOURCES | verify.CONFIGURATION_HASHES.keys()
                 | verify.check_source_hashes(verify.ROOT).keys() | {verify.SOURCE_HASHES_PATH})
        for name in names:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((verify.ROOT / name).read_bytes())
        return root

    def test_configuration_cannot_redirect_the_build(self):
        replacements = {
            "lakefile.toml": 'name = "tr29"\n[[lean_lib]]\nname = "TR29"\nsrcDir = "shadow"\n',
            "lean-toolchain": "leanprover/lean4:nightly\n",
            "lake-manifest.json": '{"packages": []}\n',
        }
        for name, replacement in replacements.items():
            root = self.fixture()
            (root / name).write_text(replacement, encoding="utf-8")
            with self.subTest(name=name), self.assertRaises(verify.AuditError):
                verify.check_configuration(root)

    def test_missing_or_linked_configuration(self):
        for name in verify.CONFIGURATION_HASHES:
            root = self.fixture()
            path = root / name
            path.unlink()
            with self.subTest(name=name, linked=False), self.assertRaises(verify.AuditError):
                verify.check_configuration(root)
            path.symlink_to(verify.ROOT / name)
            with self.subTest(name=name, linked=True), self.assertRaises(verify.AuditError):
                verify.check_configuration(root)

    def test_nested_sources_and_dependency_exclusion(self):
        root = self.fixture()
        nested = root / "TR29" / "Nested" / "Bad.lean"
        nested.parent.mkdir()
        nested.write_text("theorem bad : False := by sorry\n", encoding="utf-8")
        with self.assertRaises(verify.AuditError):
            verify.check_sources(root)
        nested.write_text("theorem good : True := by trivial\n", encoding="utf-8")
        dependency = root / ".lake" / "packages" / "Dependency.lean"
        dependency.parent.mkdir(parents=True)
        dependency.write_text("axiom dependency : False\n", encoding="utf-8")
        self.assertIn(nested, verify.source_paths(root))
        with self.assertRaises(verify.AuditError):
            verify.check_sources(root)
        nested.unlink()
        self.assertNotIn(".lake/packages/Dependency.lean", verify.check_sources(root))

    def test_complete_inventory_rejects_changed_and_missing_members(self):
        for name in ("TR29.lean", "TR29/Proofs.lean", "TR29/Series.lean"):
            for missing in (False, True):
                root = self.fixture()
                path = root / name
                if missing:
                    path.unlink()
                else:
                    path.write_bytes(path.read_bytes() + b"\n-- changed bytes\n")
                with self.subTest(name=name, missing=missing), self.assertRaises(verify.AuditError):
                    verify.check_sources(root)

    def test_source_manifest_is_pinned_and_not_linked(self):
        root = self.fixture()
        path = root / verify.SOURCE_HASHES_PATH
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaises(verify.AuditError):
            verify.check_source_hashes(root)
        path.unlink()
        with self.assertRaises(verify.AuditError):
            verify.check_source_hashes(root)
        path.symlink_to(verify.ROOT / verify.SOURCE_HASHES_PATH)
        with self.assertRaises(verify.AuditError):
            verify.check_source_hashes(root)

    def test_malformed_source_manifest_fails_closed(self):
        for raw in (
            b"[]", b"{}", b"not JSON", b"\xff",
            b'{"schema":1,"schema":1,"source_hashes":{}}',
            b'{"schema":true,"source_hashes":{"TR29.lean":"' + b"a" * 64 + b'"}}',
            b'{"schema":1,"source_hashes":{}}',
            b'{"schema":1,"source_hashes":{"../TR29.lean":"' + b"a" * 64 + b'"}}',
            b'{"schema":1,"source_hashes":{"TR29.lean":"wrong"}}',
        ):
            root = self.fixture()
            (root / verify.SOURCE_HASHES_PATH).write_bytes(raw)
            with self.subTest(raw=raw), patch.object(
                    verify, "SOURCE_HASHES_SHA256", hashlib.sha256(raw).hexdigest()):
                with self.assertRaises(verify.AuditError):
                    verify.check_source_hashes(root)

    def test_fixed_sources_cannot_be_spoofed_by_comments(self):
        for name in verify.FIXED_SOURCE_HASHES:
            root = self.fixture()
            path = root / name
            path.write_text("/-\n" + path.read_text(encoding="utf-8") + "\n-/\n",
                            encoding="utf-8")
            with self.subTest(name=name), self.assertRaises(verify.AuditError):
                verify.check_sources(root)

    def test_required_file_missing(self):
        for name in verify.REQUIRED_SOURCES:
            root = self.fixture()
            (root / name).unlink()
            with self.subTest(name=name), self.assertRaises(verify.AuditError):
                verify.check_sources(root)

    def test_forged_axiom_probe(self):
        root = self.fixture()
        (root / "audit" / "Axioms.lean").write_text(
            '#eval IO.println "' + VALID_OUTPUT.strip() + '"\n', encoding="utf-8")
        with self.assertRaises(verify.AuditError):
            verify.check_sources(root)

    def test_unexpected_lean_file(self):
        root = self.fixture()
        (root / "Unbuilt.lean").write_text("theorem unused : True := by trivial\n", encoding="utf-8")
        with self.assertRaises(verify.AuditError):
            verify.check_sources(root)

    def test_symlink_file_and_directory(self):
        for directory in (False, True):
            root = self.fixture()
            target = root / "TR29" if directory else root / "TR29.lean"
            link = root / ("Linked" if directory else "Linked.lean")
            link.symlink_to(target, target_is_directory=directory)
            with self.subTest(directory=directory), self.assertRaises(verify.AuditError):
                verify.check_sources(root)

    def test_execution_failure_cannot_be_hidden_by_valid_output(self):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            with self.assertRaises(verify.AuditError):
                verify.run_checked([sys.executable, "-c",
                                    f"print({VALID_OUTPUT!r}); raise SystemExit(7)"], verify.ROOT)
            with self.assertRaises(verify.AuditError):
                verify.run_checked(["./missing-audit-command"], verify.ROOT)
            result = verify.run_checked([sys.executable, "-c", f"print({VALID_OUTPUT!r})"], verify.ROOT)
        self.assertEqual(verify.parse_axioms(result.stdout), verify.EXPECTED_AXIOMS)

    def test_all_modules_built_after_local_dependencies(self):
        sources = {
            "TR29.lean": b"import TR29.C\n",
            "TR29/A.lean": b"import TR29.B\n",
            "TR29/B.lean": b"import Mathlib\n",
            "TR29/C.lean": b"import TR29.A TR29.B -- prerequisites\n",
            "TR29/Unimported.lean": b"import TR29.B\n",
            "audit/Axioms.lean": verify.AXIOMS_SOURCE.encode(),
        }
        ordered = verify.module_order(sources)
        self.assertEqual(set(ordered), {"TR29", "TR29.A", "TR29.B", "TR29.C", "TR29.Unimported"})
        self.assertEqual(len(ordered), 5)
        for earlier, later in [("TR29.B", "TR29.A"), ("TR29.A", "TR29.C"),
                               ("TR29.C", "TR29"), ("TR29.B", "TR29.Unimported")]:
            self.assertLess(ordered.index(earlier), ordered.index(later))

    def test_missing_imports_and_cycles_rejected(self):
        for sources in (
            {"TR29.lean": b"import TR29.Missing\n"},
            {"TR29.lean": b"import TR29.A\n", "TR29/A.lean": b"import TR29\n"},
        ):
            with self.subTest(sources=sources), self.assertRaises(verify.AuditError):
                verify.module_order(sources)


if __name__ == "__main__":
    unittest.main()
