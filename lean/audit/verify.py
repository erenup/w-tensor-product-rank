#!/usr/bin/env python3
"""Rebuild every proof module and verify the theorem's kernel dependencies."""

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parent.parent
THEOREM = "TR29.core_theorems"
EXPECTED_AXIOMS = frozenset({"propext", "Classical.choice", "Quot.sound"})
AXIOMS_SOURCE = 'import TR29\n\nexample : TR29.UnivariateMomentBound := TR29.univariate_moment_bound\nexample : TR29.GeometricKernelIdentity := TR29.geometric_kernel_identity\nexample : TR29.MatrixMomentLeadingTheorem := TR29.matrix_moment_leading\nexample : TR29.AntiDiagonalBlockTheorem := TR29.anti_diagonal_blocks\nexample : TR29.OrthogonalGramAssembly := TR29.orthogonal_gram_assembly\nexample : TR29.TR29GramLowerBound := TR29.tr29_gram_lower_bound\nexample : TR29.FiniteChartAvoidance := TR29.finite_chart_avoidance\nexample : TR29.CoreTheorems := TR29.core_theorems\n\n#print axioms TR29.univariate_moment_bound\n#print axioms TR29.geometric_kernel_identity\n#print axioms TR29.matrix_moment_leading\n#print axioms TR29.anti_diagonal_blocks\n#print axioms TR29.orthogonal_gram_assembly\n#print axioms TR29.tr29_gram_lower_bound\n#print axioms TR29.finite_chart_avoidance\n#print axioms TR29.core_theorems\n'
AXIOM_THEOREMS = ('TR29.univariate_moment_bound', 'TR29.geometric_kernel_identity', 'TR29.matrix_moment_leading', 'TR29.anti_diagonal_blocks', 'TR29.orthogonal_gram_assembly', 'TR29.tr29_gram_lower_bound', 'TR29.finite_chart_avoidance', 'TR29.core_theorems')
SOURCE_HASHES_PATH = "audit/source-hashes.json"
SOURCE_HASHES_SHA256 = '4827f28001cfe41c4dd9395416a15fe4df448cc8aa28993ddb126d1f81717105'
# Preserve the literal operations and all public hypotheses.
FIXED_SOURCE_HASHES = {'TR29/Definitions.lean': 'f1812f5918b0034be999ecaab5634aaf3a77c93a53d1f7efc4751e97435a8585', 'TR29/Statement.lean': '52d0b4a677dcb78bf68f085be728b9cd9ad6f4969cf6b1a029da6cbbebd8818a'}
CONFIGURATION_HASHES = {'lakefile.toml': 'b1921f08a58446b23f8f90a9c17ae488a46c613cd95b03bf57edbfd531c519db', 'lake-manifest.json': 'edde6bde15af135d4e16ccc6d9384081504989c1b368c3a85e58635f8e2a1ac6', 'lean-toolchain': '8190e75a201741065fe508b28955dd64dd72d090babe5f70ce6848879d68ae88'}
REQUIRED_SOURCES = frozenset({
    "TR29.lean", "TR29/Definitions.lean", "TR29/Statement.lean", "audit/Axioms.lean",
})
MODULE_PATH = re.compile(r"TR29(?:/[A-Za-z][A-Za-z0-9_]*)*\.lean\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
# Deliberately include comments, strings, and quoted identifiers in this check.
FORBIDDEN = re.compile(
    r"\b(?:sorry|sorryAx|admit|axiom|unsafe|native_decide|implemented_by|ofReduceBool|skipKernelTC|extern|set_option)\b"
)


class AuditError(Exception):
    """A verification condition failed."""


def require(condition, message):
    if not condition:
        raise AuditError(message)


def reject_forbidden(source, name):
    match = FORBIDDEN.search(source)
    require(match is None, f"Disallowed proof token in {name}: "
            f"{match.group(0) if match else ''}")


def check_configuration(root):
    """Bind the build to this source directory and the locked dependencies."""
    snapshot = {}
    for name, expected in CONFIGURATION_HASHES.items():
        path = root / name
        require(path.is_file() and not path.is_symlink(), f"Missing or linked configuration: {name}")
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == expected, f"Build configuration changed: {name}")
        snapshot[name] = data
    return snapshot


def check_source_hashes(root):
    """Require an immutable, complete inventory of proof sources."""
    path = root / SOURCE_HASHES_PATH
    require(path.is_file() and not path.is_symlink(), "Missing or linked source manifest")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SOURCE_HASHES_SHA256,
            "Source manifest does not match its SHA256 pin")

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate source-manifest field: {key}")
            result[key] = value
        return result

    try:
        binding = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise AuditError("Malformed source manifest") from error
    require(isinstance(binding, dict) and set(binding) == {"schema", "source_hashes"},
            "Unexpected source-manifest fields")
    require(type(binding["schema"]) is int and binding["schema"] == 1,
            "Unsupported source-manifest schema")
    hashes = binding["source_hashes"]
    require(isinstance(hashes, dict) and hashes, "Missing source inventory")
    for name, digest in hashes.items():
        require(isinstance(name, str) and MODULE_PATH.fullmatch(name) is not None,
                f"Invalid bound source path: {name}")
        require(isinstance(digest, str) and SHA256.fullmatch(digest) is not None,
                f"Invalid source digest: {name}")
    return hashes


def source_paths(root):
    """Enumerate recursively; dependencies are the sole source-tree exclusion."""
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "Invalid project directory")
    found = []

    def walk_error(error):
        raise AuditError(f"Cannot enumerate project sources: {error}")

    for current, directories, files in os.walk(root, onerror=walk_error, followlinks=False):
        current = Path(current)
        if current == root:
            directories[:] = [name for name in directories if name not in {".lake", ".git"}]
            files = [name for name in files if name != ".git"]
        for name in directories + files:
            path = current / name
            require(not path.is_symlink(), f"Project symlink is not allowed: {path.relative_to(root)}")
        for name in files:
            if name.endswith(".lean"):
                path = current / name
                require(path.is_file(), f"Lean source is not a regular file: {path.relative_to(root)}")
                found.append(path)
    return sorted(found)


def check_sources(root):
    """Check all Lean sources and return their bytes for a later stability check."""
    source_hashes = check_source_hashes(root)
    snapshot = {}
    for path in source_paths(root):
        name = path.relative_to(root).as_posix()
        require(name == "audit/Axioms.lean" or MODULE_PATH.fullmatch(name) is not None,
                f"Unexpected Lean source: {name}")
        data = path.read_bytes()
        try:
            source = data.decode("utf-8")
        except UnicodeDecodeError as error:
            raise AuditError(f"Lean source is not UTF-8: {name}") from error
        reject_forbidden(source, name)
        snapshot[name] = data
    require(REQUIRED_SOURCES <= snapshot.keys(),
            f"Missing required Lean sources: {sorted(REQUIRED_SOURCES - snapshot.keys())}")
    expected_sources = source_hashes.keys() | {"audit/Axioms.lean"}
    require(snapshot.keys() == expected_sources,
            f"Source inventory differs from its binding: "
            f"missing {sorted(expected_sources - snapshot.keys())}; "
            f"extra {sorted(snapshot.keys() - expected_sources)}")
    for name, expected in source_hashes.items():
        require(hashlib.sha256(snapshot[name]).hexdigest() == expected,
                f"Bound source changed: {name}")
    for name, expected in FIXED_SOURCE_HASHES.items():
        actual = hashlib.sha256(snapshot[name]).hexdigest()
        require(actual == expected, f"Fixed theorem source changed: {name}")
    require(snapshot["audit/Axioms.lean"] == AXIOMS_SOURCE.encode("utf-8"),
            "The axiom-printing source changed")
    return snapshot


def parse_axioms(stdout, stderr=""):
    require(not stderr, "Unexpected standard error from the axiom check")
    lines = stdout.strip().splitlines()
    require(len(lines) == len(AXIOM_THEOREMS), "Missing or additional axiom output")
    found = set()
    for line in lines:
        match = re.fullmatch(r"'([^']+)' depends on axioms: \[([^\[\]\r\n]*)\]", line)
        require(match is not None, "Malformed axiom output")
        theorem = match.group(1)
        require(theorem in AXIOM_THEOREMS and theorem not in found, "Missing, duplicated or unknown theorem")
        found.add(theorem)
        names = [name.strip() for name in match.group(2).split(",")]
        require(len(names) == len(EXPECTED_AXIOMS) and set(names) == EXPECTED_AXIOMS,
                f"Unexpected axiom list for {theorem}: {names}")
    require(found == set(AXIOM_THEOREMS), "Incomplete axiom audit")
    return EXPECTED_AXIOMS


def module_order(snapshot):
    """Build local dependencies first, one target at a time."""
    sources = {name[:-5].replace("/", "."): data.decode("utf-8")
               for name, data in snapshot.items() if name != "audit/Axioms.lean"}
    visited, visiting, ordered = set(), set(), []

    def visit(module):
        require(module in sources, f"Missing local import: {module}")
        require(module not in visiting, f"Local import cycle: {module}")
        if module in visited:
            return
        visiting.add(module)
        for line in sources[module].splitlines():
            match = re.match(r"\s*(?:(?:public|private)\s+)?import\s+(.+)", line)
            if match:
                for dependency in match.group(1).split("--", 1)[0].split():
                    if dependency == "TR29" or dependency.startswith("TR29."):
                        visit(dependency)
        visiting.remove(module)
        visited.add(module)
        ordered.append(module)

    for module in sorted(sources):
        visit(module)
    return ordered


PYTHON_CHILDREN = {'audit/kernel_controls.py': ['642460c8b9fd248173bc3b9f46cb93cb89b68de670affe65e1d19b3a40a9f42f', '802d5d1c2c0d0f4a4d48a8245b2a1968f053eaa8acd1fe559ebd1f7ea44b9b14', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855']}


def run_python_checked(command, root, *args, **kwargs):
    """Authenticate the complete helper program and its expected diagnostics."""
    root = Path(root)
    names = [name for name in PYTHON_CHILDREN
             if name in command or str(root / name) in command]
    require(len(names) == 1, 'Unregistered Python audit child')
    name = names[0]
    path = root / name
    source_hash, stdout_hash, stderr_hash = PYTHON_CHILDREN[name]
    def source():
        require(all(not (root / Path(*Path(name).parts[:i])).is_symlink()
                    for i in range(1, len(Path(name).parts) + 1)),
                'Linked Python audit child: ' + name)
        require(path.is_file(), 'Missing Python audit child: ' + name)
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == source_hash,
                'Python audit child source mismatch: ' + name)
        return data
    before = source()
    result = run_checked(command, root, *args, **kwargs)
    require(result.returncode == 0, 'Python audit child failed: ' + name)
    stdout, stderr = result.stdout, result.stderr
    if name == 'audit/test_verify.py':
        # unittest's duration is diagnostic; all remaining bytes are bound.
        stderr = re.sub(r'Ran (\d+) tests in [0-9.]+s',
                        r'Ran \1 tests in <time>s', stderr)
    require(hashlib.sha256(stdout.encode('utf-8')).hexdigest() == stdout_hash
            and hashlib.sha256(stderr.encode('utf-8')).hexdigest() == stderr_hash,
            'Python audit child output mismatch: ' + name)
    require(source() == before, 'Python audit child changed during execution: ' + name)
    return result


def run_checked(command, root):
    print("+ " + " ".join(command), flush=True)
    try:
        result = subprocess.run(command, cwd=root, text=True, encoding="utf-8",
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    except (OSError, UnicodeError) as error:
        raise AuditError(f"Could not execute {command[0]}: {error}") from error
    if result.stdout:
        print(result.stdout, end="", flush=True)
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr, flush=True)
    require(result.returncode == 0,
            f"Command failed with status {result.returncode}: {' '.join(command)}")
    return result


def verify(root=ROOT):
    root = Path(root)
    configuration_before = check_configuration(root)
    before = check_sources(root)
    modules = module_order(before)
    # Naming the package preserves the downloaded dependency cache.
    run_checked(["lake", "clean", "tr29"], root)
    for module in modules:
        run_checked(["lake", "build", module], root)
    result = run_checked(["lake", "env", "lean", "audit/Axioms.lean"], root)
    parse_axioms(result.stdout, result.stderr)
    run_python_checked([sys.executable, "-B", "audit/kernel_controls.py"], root)
    require(check_sources(root) == before, "Lean sources changed during verification")
    require(check_configuration(root) == configuration_before,
            "Build configuration changed during verification")
    print(f"PASS: rebuilt {len(modules)} proof modules; all project Lean sources checked.")
    print("PASS: complete source inventory and SHA256 binding match.")
    print(f"PASS: {THEOREM} and seven further probes use exactly propext, Classical.choice, Quot.sound.")


def main():
    try:
        verify()
    except (AuditError, OSError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
