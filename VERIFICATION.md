# Verification and mathematical scope

The paper proves the quantified rank formulas. The Lean core proves seven
universal algebraic targets, and the Python suites check finite exact
instances and required rejections. These forms of evidence have the
separate scopes recorded below and in the [result map](paper-lean-mapping/by-section.md).

## Exact finite checks

From the repository root with Python 3.11 or later:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
```

Both commands completed with exit zero, empty stderr, and identical stdout:
SHA256 `554e38c08ba26f380e922ab4b6fe18f61cd344468bd0f1737313b10d5bb3f853`.
Each command prints:

```text
PASS: check_charts.py (normal, optimized, hash-seed)
PASS: exact_cyclotomic.py (normal, optimized, hash-seed)
PASS: check_exact.py (normal, optimized, hash-seed)
PASS: 8 upper examples; 3 cubatures; 24 inline negative-control executions; 3 proof bindings
RESULT: PASS TR-29 binary-monomial product verification
PASS: 15 inline negative-control executions; 2 proof bindings
RESULT: PASS TR-29 verification
```

The W suite includes rational degree-2-through-9 tests, all 64 coefficients
and moments of a 20-term cubic decomposition over a cyclotomic field,
and an invertible Gram matrix at an asymmetric finite chart. Its five
inline rejection controls run in three modes. The binary-monomial suite
checks eight character decompositions, three rational cubatures, and
finite Laurent identities, including zero and repeated nodes. Its eight
inline controls run in three modes. Every checker output and required
rejection is bound; absent or changed controls cannot be accepted merely
by recomputing a manifest. The parent authenticates the child suite.

See the [W suite](verification/README.md) and
[binary-monomial suite](families/monomial-products/verification/README.md)
for exact inventories, finite parameter ranges, and input integrity rules.
These computations use no approximate rank decisions. They do not prove
the universal moment theorem or all-parameter character construction.

## Seven universal algebraic targets in Lean

The toolchain is Lean `v4.34.0-rc2`; Mathlib is pinned to
`85e3a25e006c35636f0e53b0e9296caca2685bc0`. With the toolchain installed:

```sh
cd lean
lake exe cache get
python3 -B verify
```

The launcher passed all 17 source and execution controls under normal
and optimized Python, comparing all diagnostics after normalizing only
unittest's elapsed-duration field. It then rebuilt all nine project
modules, checked eight literal target types and eight transitive axiom
closures, and ran one positive and seven false mathematical controls.
The positive control passed; every false control failed for the required
mathematical reason. All axiom closures were exactly `propext`,
`Classical.choice`, and `Quot.sound`.

The recorded fresh audit took about 75 seconds and peaked at 3.17 GiB
resident memory, using two workers and an 8 GiB memory limit. Project
proof objects were rebuilt; the pinned dependency cache was retained.
Dependency download time is separate. The verifier cleans only its own
project before rebuilding.

The seven targets are the univariate moment bound, geometric inverse,
matrix-moment leading determinant theorem, anti-diagonal block theorem,
orthogonal Gram assembly, W-count under explicit Gram hypotheses, and
finite chart avoidance. Their exact quantifiers are in
[Statement.lean](lean/TR29/Statement.lean), and their boundaries are in
[SCOPE.md](lean/SCOPE.md). The aggregate does not state either full rank
formula. Specific multivariate vectors and cancellation, the
rational/series/numerator identification, arbitrary-decomposition
reduction, the general binary count, and the character construction
remain in the written proof.

## Paper-to-proof correspondence

```sh
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
```

The correspondence checker validates numbered paper labels and result
numbers, actual Lean declarations and their proposition types, and exact
Python function references. Its mutation controls require invalid links
and unsupported coverage claims to fail. This structural check does not
compile Lean or prove a paper-only assertion. The
[section table](paper-lean-mapping/by-section.md) and the machine-readable
[mapping](paper-lean-mapping/mapping.json) state the coverage per result.

Both commands completed with exit zero, empty stderr, and identical stdout:
SHA256 `b25f8bc58afdf7da46c01c2a52b6556e536d5e585ac9c04274b5cb8f15fc2271`.

```text
PASS: 12 numbered results in 6 paper sections
PASS: 7 algebraic Lean targets and their aggregate declaration
PASS: 5 exact-check links and 9 supporting paper anchors
PASS: 20 mapping negative controls
RESULT: PASS mapping structure; mathematical coverage is stated per entry
```

## Manuscript and Markdown

From `paper/`, with the packages in the source installed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The included [PDF](paper/main.pdf) builds to 12 pages. The final LaTeX
log has no warnings, undefined references, or overfull/underfull boxes.
Authors and acknowledgements are TBD. LaTeX engine timestamps can change
PDF bytes on another build; hashes bind the included PDF.

From the repository root:

```sh
python3 -I -B tools/check_markdown_math.py
python3 -I -B -O tools/check_markdown_math.py
```

This standard-library guard scans every tracked Markdown file and runs
acceptance/rejection controls in both modes. It checks the repository's
static profile for math macros, norm delimiters, environments, dollar
math, and raw inline comparison characters. It is not a complete
Markdown/TeX parser or a live renderer test.

## Integrity

```sh
sha256sum -c MANIFEST.sha256
(cd paper && sha256sum -c SHA256SUMS)
(cd verification && sha256sum -c SHA256SUMS)
(cd families/monomial-products/verification && sha256sum -c SHA256SUMS)
```

The root manifest binds every tracked file except itself, including the
PDF and nested manifests. The exact-check runners also enforce their own
inventories and fixed source/control bindings. The Lean verifier binds
the exact definitions, statements, proofs and dependency configuration.
Generated build directories and dependency caches are excluded from the
repository inventory.
