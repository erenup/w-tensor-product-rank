#!/usr/bin/env python3
"""Bind exact finite checks and proofs; require all original controls in three modes."""
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).absolute().parent
MODES = [('normal', [], '1'), ('optimized', ['-O'], '1'),
         ('hash-seed', [], '8675309')]
MONOMIAL_RUNNER_SHA256 = 'ee771aca2a6c25108f28bab0eb8fb3b6058c80ab0e1469e8fb47eb1c5047936f'
MONOMIAL_OUTPUT_SHA256 = 'f413bccde2ddc6df48949fb9d28496a484b0e3f91e6c694d04702e8c3609e0d7'
SCRIPT_HASHES = {
    'check_charts.py': 'fbc5a267ce722966ef63c0387df6c5cab316c48fcc97165f05b0003affc0c140',
    'exact_cyclotomic.py': 'f12d9ea5ac551f0b1b3c585c7b4c42e7c5984e5b9173d526a7be8572f533d993',
}
SOURCE_PROOF_HASHES = {
    'PROOF.md': '057019569f205b359f4a3da3caf30ac3a2fdf5a425cc783ce2f172c7cbd69497',
    'STATEMENT.md': 'd5696bc8ad685a5d8167103debd76430f5c3cb7aadcf9e9037f620f8a96fafa6',
}
CONTROLS = {
    'check_charts.py': [
        {'label': 'change one upper-decomposition coefficient', 'rejection': 'U-W orthogonality'},
        {'label': 'choose a chart with a pole', 'rejection': 'chart pole'},
        {'label': 'incorrectly presume every chart is good', 'rejection': 'chart block nondegeneracy'},
    ],
    'exact_cyclotomic.py': [
        {'label': 'omit one summand', 'rejection': 'coefficient (0, 0, 0)'},
        {'label': 'wrong summand coefficient', 'rejection': 'coefficient (0, 0, 0)'},
    ],
}
EXPECTED_FILES = set(SCRIPT_HASHES) | {
    'run.py', 'README.md', 'CHECKERS.txt', 'NEGATIVE_CONTROLS.json',
    'SOURCE_BINDINGS.txt', 'SHA256SUMS',
}


def need(ok, message):
    if not ok:
        raise SystemExit('FAIL: ' + message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def reject_number(value):
    raise SystemExit('FAIL: non-integer JSON number: ' + value)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        need(key not in result, 'duplicate JSON key')
        result[key] = value
    return result


def read_json(data):
    return json.loads(data, object_pairs_hook=unique_pairs,
                      parse_float=reject_number, parse_constant=reject_number)


def inventory():
    need(HERE.is_dir() and not HERE.is_symlink(), 'invalid verification directory')
    files = {}
    for path in HERE.iterdir():
        need(path.is_file() and not path.is_symlink(), 'invalid verification file: ' + path.name)
        need(path.stat().st_size <= 4500000, 'file size: ' + path.name)
        files[path.name] = path.read_bytes()
    need(set(files) == EXPECTED_FILES, 'verification file coverage')
    return files


def proof_inventory():
    root = HERE.parent / 'proofs'
    need(root.is_dir() and not root.is_symlink(), 'invalid proof directory')
    paths = list(root.iterdir())
    need({p.name for p in paths} == set(SOURCE_PROOF_HASHES), 'proof coverage')
    need(all(p.is_file() and not p.is_symlink() for p in paths), 'invalid proof file')
    return {p.name: digest(p.read_bytes()) for p in paths}


def validate_bindings(data):
    included = {}
    for line in data.decode().splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        parts = line.split()
        need(len(parts) == 3 and all(re.fullmatch('[0-9a-f]{64}', x) for x in parts[:2]),
             'proof binding syntax')
        source, curated, name = parts
        need(name not in included, 'duplicate proof binding')
        need(SOURCE_PROOF_HASHES.get(name) == source, 'source proof hash mismatch')
        included[name] = curated
    need(included == proof_inventory(), 'proof binding mismatch')
    return included


def validate_script(name, data):
    need(digest(data) == SCRIPT_HASHES[name], 'source script mismatch: ' + name)
    allowed = {'copy', 'fractions', 'itertools', 'math', 'json', 'sys', 'exact_cyclotomic'}
    forbidden = {'float', 'complex', 'eval', 'exec', 'compile', '__import__', 'getattr'}
    tree = ast.parse(data.decode(), filename=name)
    for node in ast.walk(tree):
        need(not isinstance(node, ast.Assert), 'assert in ' + name)
        if isinstance(node, ast.Import):
            need(all(alias.name in allowed for alias in node.names), 'unexpected import in ' + name)
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0 and node.module in allowed, 'unexpected import in ' + name)
            if node.module == 'math':
                need(all(alias.name == 'comb' for alias in node.names), 'non-integer math import')
        elif isinstance(node, ast.Constant):
            need(type(node.value).__name__ not in {'float', 'complex'}, 'inexact literal in ' + name)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in forbidden, 'inexact or dynamic call in ' + name)


def validate_directory():
    files = inventory()
    sums = {}
    for line in files['SHA256SUMS'].decode().splitlines():
        parts = line.split('  ', 1)
        need(len(parts) == 2 and re.fullmatch('[0-9a-f]{64}', parts[0]), 'manifest syntax')
        sha, name = parts
        need(name not in sums, 'duplicate manifest entry')
        sums[name] = sha
    need(set(sums) == set(files) - {'SHA256SUMS'}, 'manifest coverage')
    for name, sha in sums.items():
        need(digest(files[name]) == sha, 'manifest mismatch: ' + name)
    registry = {}
    for line in files['CHECKERS.txt'].decode().splitlines():
        parts = line.split()
        need(len(parts) == 2 and parts[0] in SCRIPT_HASHES
             and re.fullmatch('[0-9a-f]{64}', parts[1]), 'checker registry syntax')
        name, expected = parts
        need(name not in registry, 'duplicate checker')
        registry[name] = expected
    need(set(registry) == set(SCRIPT_HASHES), 'checker coverage')
    need(read_json(files['NEGATIVE_CONTROLS.json']) == CONTROLS, 'negative-control definitions')
    for name in sorted(SCRIPT_HASHES):
        validate_script(name, files[name])
    proofs = validate_bindings(files['SOURCE_BINDINGS.txt'])
    return registry, proofs, {name: digest(data) for name, data in files.items()}


def validate_result(name, data):
    result = read_json(data)
    need(type(result) is dict and result.get('status') == 'PASS', 'checker result status: ' + name)
    key = 'controls' if name == 'check_charts.py' else 'negative_controls'
    need(result.get(key) == CONTROLS[name], 'inline control coverage: ' + name)
    if name == 'check_charts.py':
        need(set(result) == {'status', 'univariate', 'cubic_triple', 'controls', 'scope'},
             'chart result fields')
        cases = result['univariate']
        need(type(cases) is list and len(cases) == 8, 'univariate degree coverage')
        for degree, entry in zip(range(2, 10), cases):
            need(type(entry) is dict and set(entry) == {'d', 'gamma', 'H_at_2', 'block_rank'},
                 'univariate result fields')
            need(type(entry['d']) is int and entry['d'] == degree
                 and type(entry['block_rank']) is int and entry['block_rank'] == degree - 2,
                 'univariate degree or rank')
            need(type(entry['gamma']) is str and type(entry['H_at_2']) is str,
                 'univariate exact output format')
        need(result['cubic_triple'] == {'chart': [2, 3, 4], 'U_rank': 8,
             'V_Gram_ranks': [4, 4, 4], 'full_Gram_rank': 20}, 'cubic chart coverage')
        need(result['scope'] == 'finite exact regressions only; universal lower bound is PROOF.md',
             'checker scope')
    else:
        need(set(result) == {'status', 'field', 'summands', 'coefficients_checked', 'moments_checked',
             'hilbert_ranks', 'pair_intersections', 'triple_intersection', 'sum_W_dimension',
             'sum_W_Gram_rank', 'negative_controls'}, 'cyclotomic result fields')
        need(result['field'] == 'Q[z]/(z^4-z^3+z^2-z+1)' and result['summands'] == 20
             and result['coefficients_checked'] == 64 and result['moments_checked'] == 64,
             'cyclotomic coefficient coverage')
        need(result['hilbert_ranks'] == {'(1, 1, 1)': 8, '(2, 1, 1)': 12,
             '(1, 2, 2)': 16, '(2, 2, 2)': 20} and result['pair_intersections'] == [2, 2, 2]
             and result['triple_intersection'] == 1 and result['sum_W_dimension'] == 7
             and result['sum_W_Gram_rank'] == 3, 'cyclotomic rank coverage')
    return len(CONTROLS[name])


MONOMIAL_MANIFEST_SHA256 = 'c23864d9ec7d26b795d4c8a8046d7008111ceda953e753a02a37228f2409bae5'


def authenticate_child_manifest(verification, expected, label):
    manifest = verification / 'SHA256SUMS'
    need(manifest.is_file() and not manifest.is_symlink(), label+' missing regular manifest')
    need(digest(manifest.read_bytes()) == expected, label+' manifest binding mismatch')


def run_monomial_products():
    families = HERE.parent / 'families'
    root = families / 'monomial-products'
    verification = root / 'verification'
    runner = verification / 'run.py'
    need(all(path.is_dir() and not path.is_symlink() for path in [families, root, verification])
         and runner.is_file() and not runner.is_symlink(), 'missing monomial product runner')
    need(digest(runner.read_bytes()) == MONOMIAL_RUNNER_SHA256, 'monomial product runner source mismatch')
    authenticate_child_manifest(verification, MONOMIAL_MANIFEST_SHA256, 'monomial product')
    try:
        result = subprocess.run([sys.executable, '-S', '-s', '-B', str(runner)], cwd=HERE,
                                env={'PATH': os.defpath, 'LC_ALL': 'C.UTF-8', 'PYTHONHASHSEED': '1'},
                                stdin=subprocess.DEVNULL, capture_output=True, timeout=600)
    except subprocess.TimeoutExpired:
        raise SystemExit('FAIL: monomial product suite timeout')
    need(result.returncode == 0 and not result.stderr, 'monomial product suite failed')
    need(digest(result.stdout) == MONOMIAL_OUTPUT_SHA256, 'monomial product output hash mismatch')
    need(runner.is_file() and not runner.is_symlink()
         and digest(runner.read_bytes()) == MONOMIAL_RUNNER_SHA256,
         'monomial product runner changed during execution')
    authenticate_child_manifest(verification, MONOMIAL_MANIFEST_SHA256, 'monomial product')
    print(result.stdout.decode(), end='')


def main():
    registry, proofs, before = validate_directory()
    negative_count = 0
    for name, expected in sorted(registry.items()):
        previous = None
        for mode, flags, seed in MODES:
            command = [sys.executable, '-S', '-s', '-B'] + flags + [str(HERE / name)]
            env = {'PATH': os.defpath, 'LC_ALL': 'C.UTF-8', 'PYTHONHASHSEED': seed}
            try:
                result = subprocess.run(command, cwd=HERE, env=env, stdin=subprocess.DEVNULL,
                                        capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                raise SystemExit('FAIL: checker timeout: ' + name + ' ' + mode)
            need(result.returncode == 0, 'checker exit status: ' + name + ' ' + mode)
            need(not result.stderr, 'checker standard error: ' + name + ' ' + mode)
            need(digest(result.stdout) == expected, 'output hash mismatch: ' + name + ' ' + mode)
            need(previous is None or previous == result.stdout, 'checker mode mismatch: ' + name)
            negative_count += validate_result(name, result.stdout)
            previous = result.stdout
        print('PASS: ' + name + ' (normal, optimized, hash-seed)')
    run_monomial_products()
    need({name: digest(data) for name, data in inventory().items()} == before,
         'verification files changed during execution')
    need(proof_inventory() == proofs, 'proof files changed during execution')
    need(negative_count == 15, 'total inline control coverage')
    print('PASS: 15 inline negative-control executions; 2 proof bindings')
    print('RESULT: PASS TR-29 verification')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, SyntaxError, UnicodeError) as error:
        raise SystemExit('FAIL: verification input: ' + type(error).__name__)
