# Exact binary-monomial product regressions

Run from this directory with Python 3.11 or later:

```sh
python3 -S -s -B run.py
```

The unchanged `check_exact.py` and `fixtures.json` use only standard-library
integer, rational and cyclotomic-polynomial arithmetic. The checker enumerates
every multihomogeneous coefficient in eight fixed upper examples. These include
the 54-term triple product of x^3 y^2, unequal exponents, balanced factors,
four blocks, and one-block, two-block and cubic-W overlaps. Character sums are
reduced exactly modulo the corresponding cyclotomic polynomial.

Three fixed rational cubatures directly evaluate all Gram entries and a
nonzero full determinant. Their vector-list lengths are 33, 54 and 13.
They include zero coordinates, a repeated node with two nonzero weights,
unequal exponents, a balanced factor and a V block of length two. The checker
also verifies the finite Laurent identity at zero, positive and negative
rational nodes.

These are finite supporting regressions. The [written proof](../proofs/PROOF.md)
establishes the full quantified lower bound and the all-parameter character
construction; finite examples do not classify all supports or prove the
universal lattice-avoidance lemma. No real, border, cactus, regrouped-mode or
unrestricted nonsymmetric rank conclusion is checked here.

## Controls and execution

Eight original inline controls corrupt a claimed rank, transpose the lattice,
omit or corrupt a character, alter the target phase, change a cubature weight,
repeat a Gram vector, or reverse the Laurent remainder sign. All eight exact
labels and rejection diagnostics in
[NEGATIVE_CONTROLS.json](NEGATIVE_CONTROLS.json) are mandatory.

The runner executes the checker normally, under `-O`, and with a second hash
seed. Every run must exit zero, have empty stderr, and produce byte-identical
stdout matching [CHECKERS.txt](CHECKERS.txt). Strict JSON validation checks all
eight control outcomes and the exact finite fixture coverage. Thus each runner
call includes three positive executions and 24 inline control executions.
The environment is restricted, site initialization and bytecode writes are
disabled, and each checker invocation has a 120-second timeout.

[SHA256SUMS](SHA256SUMS) covers every verification file except itself. The
runner enforces exact file, checker and control inventories, rejects symlinks
and extra directories, and pins the original checker and fixture bytes
independently of that manifest. Removing controls or fixtures fails even after
recomputing manifest hashes. Exactness checks reject assertions, inexact
literals, unsupported imports and dynamic execution; JSON must have unique
keys and integral numeric values.

[SOURCE_BINDINGS.txt](SOURCE_BINDINGS.txt) binds the source identifiers and
included bytes of the statement, proof and literature discussion. The runner
checks the complete three-file proof inventory and rechecks all verification
and proof hashes after execution. Every failure exits nonzero under normal
and optimized Python. The main TR-29 runner invokes this suite and propagates
any failure.
