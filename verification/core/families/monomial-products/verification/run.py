#!/usr/bin/env python3
"""Bind binary-monomial proof inputs and replay exact finite controls in three modes."""
import ast
import hashlib
import json
from math import prod
import os
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).absolute().parent
MODES = [('normal', [], '1'), ('optimized', ['-O'], '1'),
         ('hash-seed', [], '8675309')]
INPUT_HASHES = {
    'check_exact.py': '02f78ee1a91bf32ccef94cf1cf263c4c3948e304a9f904bf87b187259aeac533',
    'fixtures.json': '4ddc4c7215b97ab8226e0f3624be22f2a496e41af59721013e91e338653cfd3d',
}
SOURCE_PROOF_HASHES = {
    'STATEMENT.md': '91ea0edc48c07f4b1a14bf2d397f003973d7c0a82d860dad808aad2c254cfa8e',
    'PROOF.md': '9f8351f57130f69f631827c7805f16cbca6a15e3054d1fdd7b69c4e972b73fe6',
    'LITERATURE.md': '4d9f1a98d4db41aae2c7df2f745aa74058c4c6a07efaa00e06c90673ce84e363',
}
CONTROLS = [
    {'control': 'wrong claimed rank', 'rejected': 'REJECT: claimed rank'},
    {'control': 'transpose', 'rejected': 'REJECT: coefficient-box lattice collision'},
    {'control': 'remove_character', 'rejected': 'REJECT: actual cyclotomic coefficient sum'},
    {'control': 'corrupt_character', 'rejected': 'REJECT: actual cyclotomic coefficient sum'},
    {'control': 'phase', 'rejected': 'REJECT: actual cyclotomic coefficient sum'},
    {'control': 'weight', 'rejected': 'REJECT: cubature moment'},
    {'control': 'duplicate_vector', 'rejected': 'REJECT: full evaluated Gram determinant'},
    {'control': 'laurent_sign', 'rejected': 'REJECT: finite Laurent division identity'},
]
EXPECTED_FILES = set(INPUT_HASHES) | {
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
        need(len(parts) == 3 and all(re.fullmatch('[0-9a-f]{64}', value) for value in parts[:2]),
             'proof binding syntax')
        source, curated, name = parts
        need(name not in included, 'duplicate proof binding')
        need(SOURCE_PROOF_HASHES.get(name) == source, 'source proof hash mismatch')
        included[name] = curated
    need(included == proof_inventory(), 'proof binding mismatch')
    return included


def validate_checker(data):
    allowed = {'argparse', 'copy', 'fractions', 'functools', 'itertools', 'json', 'math', 'pathlib'}
    forbidden = {'float', 'complex', 'eval', 'exec', 'compile', '__import__', 'getattr'}
    for node in ast.walk(ast.parse(data.decode(), filename='check_exact.py')):
        need(not isinstance(node, ast.Assert), 'assert in checker')
        if isinstance(node, ast.Import):
            need(all(alias.name in allowed for alias in node.names), 'unexpected checker import')
        elif isinstance(node, ast.ImportFrom):
            need(node.level == 0 and node.module in allowed, 'unexpected checker import')
            if node.module == 'math':
                need(all(alias.name in {'comb', 'prod'} for alias in node.names), 'non-integer math import')
        elif isinstance(node, ast.Constant):
            need(type(node.value).__name__ not in {'float', 'complex'}, 'inexact checker literal')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            need(node.func.id not in forbidden, 'inexact or dynamic checker call')


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
    for name, sha in INPUT_HASHES.items():
        need(digest(files[name]) == sha, 'source input mismatch: ' + name)
    registry = files['CHECKERS.txt'].decode().splitlines()
    need(len(registry) == 1, 'checker coverage')
    parts = registry[0].split()
    need(len(parts) == 2 and parts[0] == 'check_exact.py'
         and re.fullmatch('[0-9a-f]{64}', parts[1]), 'checker registry syntax')
    need(read_json(files['NEGATIVE_CONTROLS.json']) == CONTROLS, 'negative-control definitions')
    fixtures = read_json(files['fixtures.json'])
    need(type(fixtures) is dict and set(fixtures) == {'upper', 'lower'}, 'fixture fields')
    need(len(fixtures['upper']) == 8 and len(fixtures['lower']) == 3, 'fixture coverage')
    validate_checker(files['check_exact.py'])
    proofs = validate_bindings(files['SOURCE_BINDINGS.txt'])
    return parts[1], fixtures, proofs, {name: digest(data) for name, data in files.items()}


def validate_result(data, fixtures):
    result = read_json(data)
    need(type(result) is dict and set(result) == {'status', 'scope', 'upper', 'lower', 'negative_controls'},
         'checker result fields')
    need(result['status'] == 'PASS' and result['scope'] == 'finite exact regressions only',
         'checker result status or scope')
    need(result['negative_controls'] == CONTROLS, 'inline control coverage')
    expected_upper = [{'a': case['a'], 'b': case['b'], 'rank': case['rank'],
                       'coefficients': prod(a + b + 1 for a, b in zip(case['a'], case['b']))}
                      for case in fixtures['upper']]
    expected_lower = [{'d': case['d'], 'b': case['b'], 'rank': case['rank'],
                       'nodes_with_repeat': prod(d + 1 for d in case['d']) + 1,
                       'zero_coordinates': True, 'Gram_determinant_nonzero': True}
                      for case in fixtures['lower']]
    need(result['upper'] == expected_upper, 'upper coefficient coverage')
    need(result['lower'] == expected_lower, 'lower Gram coverage')


def main():
    expected, fixtures, proofs, before = validate_directory()
    previous = None
    for mode, flags, seed in MODES:
        command = [sys.executable, '-S', '-s', '-B'] + flags + [str(HERE / 'check_exact.py')]
        env = {'PATH': os.defpath, 'LC_ALL': 'C.UTF-8', 'PYTHONHASHSEED': seed}
        try:
            result = subprocess.run(command, cwd=HERE, env=env, stdin=subprocess.DEVNULL,
                                    capture_output=True, timeout=120)
        except subprocess.TimeoutExpired:
            raise SystemExit('FAIL: checker timeout: ' + mode)
        need(result.returncode == 0, 'checker exit status: ' + mode)
        need(not result.stderr, 'checker standard error: ' + mode)
        need(digest(result.stdout) == expected, 'output hash mismatch: ' + mode)
        need(previous is None or previous == result.stdout, 'checker mode mismatch')
        validate_result(result.stdout, fixtures)
        previous = result.stdout
    need({name: digest(data) for name, data in inventory().items()} == before,
         'verification files changed during execution')
    need(proof_inventory() == proofs, 'proof files changed during execution')
    print('PASS: check_exact.py (normal, optimized, hash-seed)')
    print('PASS: 8 upper examples; 3 cubatures; 24 inline negative-control executions; 3 proof bindings')
    print('RESULT: PASS TR-29 binary-monomial product verification')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, TypeError, KeyError, SyntaxError, UnicodeError) as error:
        raise SystemExit('FAIL: verification input: ' + type(error).__name__)
