#!/usr/bin/env python3
"""Single entry point for the exact checks of this repository.

Every file under verification/ is authenticated against verification/SHA256SUMS.
The child runners and their manifests are bound by digest. Each child runner
is executed in normal, optimized and alternate hash-seed modes with a clean
environment; it must exit 0, write nothing to standard error, and give the same
recorded output in every mode. Integrity controls that alter the inventory must
be rejected. Python standard library only; run from any directory with
python3 -S -s -B verification/run.py (the same result is required under -O).
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LABEL = 'TR-29'
MODES = [('normal', [], '1'), ('optimized', ['-O'], '1'),
         ('hash-seed', [], '8675309')]
# (child runner, child manifest, runner sha256, manifest sha256, stdout sha256),
# paths relative to verification/
CHILDREN = [
    ('core/verification/run.py',
     'core/verification/SHA256SUMS',
     'a4ad9ba2d4e5c4e3b42800c0c59af25edb6a701440391c57512860c35f62d71e',
     '8255a3accae73932f4b7efe021d730d72667f29066d100bc1f0b2e9055ee2313',
     '554e38c08ba26f380e922ab4b6fe18f61cd344468bd0f1737313b10d5bb3f853'),
]


def need(condition, message):
    if not condition:
        raise SystemExit('FAIL: ' + message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    files = {}
    for path in sorted(HERE.rglob('*')):
        name = path.relative_to(HERE).as_posix()
        need(not path.is_symlink(), 'symbolic link: ' + name)
        need('__pycache__' not in path.parts, 'bytecode cache: ' + name)
        if path.is_file():
            files[name] = path.read_bytes()
    return files


def manifest_bytes(files):
    return ''.join(digest(data) + '  ' + name + '\n'
                   for name, data in sorted(files.items())
                   if name != 'SHA256SUMS').encode()


def validate(files):
    need('SHA256SUMS' in files, 'missing manifest')
    manifest = {}
    for line in files['SHA256SUMS'].decode().splitlines():
        parts = line.split('  ', 1)
        need(len(parts) == 2 and len(parts[0]) == 64
             and all(c in '0123456789abcdef' for c in parts[0]),
             'manifest syntax')
        need(parts[1] not in manifest, 'duplicate manifest entry')
        manifest[parts[1]] = parts[0]
    need(set(manifest) == set(files) - {'SHA256SUMS'}, 'manifest coverage')
    for name, sha in sorted(manifest.items()):
        need(digest(files[name]) == sha, 'manifest mismatch: ' + name)
    for runner, child_manifest, runner_sha, manifest_sha, _ in CHILDREN:
        need(digest(files.get(runner, b'')) == runner_sha,
             'child runner binding: ' + runner)
        need(digest(files.get(child_manifest, b'')) == manifest_sha,
             'child manifest binding: ' + child_manifest)


def controls(files):
    runner, child_manifest = CHILDREN[0][0], CHILDREN[0][1]
    cases = []
    changed = dict(files)
    changed[runner] = files[runner] + b'\n# changed bytes\n'
    cases.append((changed, 'manifest mismatch: ' + runner))
    rebound = dict(changed)
    rebound['SHA256SUMS'] = manifest_bytes(rebound)
    cases.append((rebound, 'child runner binding: ' + runner))
    changed = dict(files)
    changed[child_manifest] = files[child_manifest] + b'\n'
    changed['SHA256SUMS'] = manifest_bytes(changed)
    cases.append((changed, 'child manifest binding: ' + child_manifest))
    missing = dict(files)
    del missing[runner]
    cases.append((missing, 'manifest coverage'))
    extra = dict(files)
    extra['unregistered.txt'] = b'extra\n'
    cases.append((extra, 'manifest coverage'))
    duplicate = dict(files)
    duplicate['SHA256SUMS'] = (files['SHA256SUMS']
                               + files['SHA256SUMS'].splitlines(keepends=True)[0])
    cases.append((duplicate, 'duplicate manifest entry'))
    for packet, expected in cases:
        try:
            validate(packet)
        except SystemExit as error:
            need(str(error) == 'FAIL: ' + expected,
                 'integrity control message: ' + expected)
            continue
        raise SystemExit('FAIL: integrity control accepted: ' + expected)
    return len(cases)


def execute(runner, flags, seed, label):
    command = [sys.executable, '-S', '-s', '-B', *flags, str(HERE / runner)]
    try:
        return subprocess.run(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                              capture_output=True, timeout=3600,
                              env={'PATH': os.defpath, 'LC_ALL': 'C.UTF-8',
                                   'PYTHONHASHSEED': seed})
    except subprocess.TimeoutExpired:
        raise SystemExit('FAIL: timeout: ' + runner + ' (' + label + ')')


def main():
    files = inventory()
    validate(files)
    rejected = controls(files)
    for runner, _, _, _, stdout_sha in CHILDREN:
        outputs = set()
        for label, flags, seed in MODES:
            result = execute(runner, flags, seed, label)
            need(result.returncode == 0,
                 'child exit status: ' + runner + ' (' + label + ')')
            need(not result.stderr,
                 'child standard error: ' + runner + ' (' + label + ')')
            outputs.add(result.stdout)
        need(len(outputs) == 1, 'child output differs across modes: ' + runner)
        stdout = outputs.pop()
        need(digest(stdout) == stdout_sha, 'child standard output: ' + runner)
        sys.stdout.write(stdout.decode())
        print('PASS: ' + runner + ' (normal, optimized, hash-seed)')
    print('PASS: %d files authenticated; %d integrity controls rejected'
          % (len(files), rejected))
    print('RESULT: PASS ' + LABEL + ' exact verification')


if __name__ == '__main__':
    main()
