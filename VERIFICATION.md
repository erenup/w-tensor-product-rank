# Verification

The two rank formulas, Theorem 1.1 and Theorem 8.1 of the
[paper](paper/main.pdf), are proved in the paper. The Lean core proves
seven universal algebraic targets with the scope recorded in
[lean/SCOPE.md](lean/SCOPE.md), and the Python suites check finite exact
instances and required rejections. The [result map](paper-lean-mapping/by-section.md)
states the evidence for each numbered result. The Python outputs below
were observed on 2026-11-01 with Python 3.12 from the repository root.
All Python programs use only the standard library.

## Exact supporting computations

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
```

Both commands exited successfully, with empty standard error and
byte-identical standard output:

```text
PASS: check_charts.py (normal, optimized, hash-seed)
PASS: exact_cyclotomic.py (normal, optimized, hash-seed)
PASS: check_exact.py (normal, optimized, hash-seed)
PASS: 8 upper examples; 3 cubatures; 24 inline negative-control executions; 3 proof bindings
RESULT: PASS TR-29 binary-monomial product verification
PASS: 15 inline negative-control executions; 2 proof bindings
RESULT: PASS TR-29 verification
PASS: core/verification/run.py (normal, optimized, hash-seed)
PASS: 31 files authenticated; 6 integrity controls rejected
RESULT: PASS TR-29 exact verification
```

The standard-output SHA-256 is
`b66cea20c52ef24ced83f233541e7ad1f8a4f88efc0615bba4a3297d806f3ae1`.

The entry point authenticates all 25 files in `verification/`, its
[manifest](verification/SHA256SUMS) included, binds the child runner
`verification/core/verification/run.py` and its manifest by digest, runs
the child in normal, optimized and alternate hash-seed modes with the
same recorded output, and rejects six altered inventories. The child
runs `check_charts.py` and `exact_cyclotomic.py` in the same three
modes; together they check rational one-coordinate examples in degrees
2 to 9, all 64 coefficients and 64 moments of one 20-term decomposition
of the cubic triple over a cyclotomic field, and a nonsingular
$`20\times20`$ Gram matrix for it at chart parameters $(2,3,4)$. Their
five inline controls run in three modes (15 executions), and the two
files of `verification/core/proofs/` are bound by hash. The child then
authenticates and runs the binary-monomial suite in
`verification/core/families/monomial-products/verification/`, which
checks every coefficient of eight character decompositions, three
rational cubatures with full Gram matrices including zero coordinates
and a repeated point, and the finite division identity at selected
nodes. Its eight inline controls run in three modes (24 executions),
and its three proof files are bound by hash. The computations use
integer, rational and cyclotomic arithmetic and no approximate rank
decisions. They do not prove the universal moment theorem or the
all-parameter character construction. See the
[exact-check guide](verification/README.md), the
[W-suite guide](verification/core/verification/README.md) and the
[binary-monomial suite guide](verification/core/families/monomial-products/verification/README.md).

## Paper-to-Lean mapping

```sh
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
```

Both commands exited successfully, with empty standard error and
byte-identical standard output:

```text
PASS: paper title, authors, 10 numbered section titles and 31 numbered results in TeX order
PASS: 7 algebraic Lean targets and their aggregate declaration
PASS: 5 exact-check links and 14 supporting paper anchors
PASS: by-section tables and section headings agree with the map
PASS: 38 mapping negative controls
RESULT: PASS mapping structure; mathematical coverage is stated per entry
```

The standard-output SHA-256 is
`8dbf56e7a9f401c1fbd4501645865227f3c184d1d94363b0b5967597475fc415`.
The checker reconstructs the paper title, subtitle and authors, the
eight numbered sections and two appendices, and all 31 numbered results
with their per-environment section numbers and bracketed names, and
requires each to agree with [mapping.json](paper-lean-mapping/mapping.json).
Mapped Lean declarations must exist with their proposition types and be
registered in the exact-type and axiom probes of `lean/audit/Axioms.lean`;
mapped exact-check functions must exist in the three checkers under
`verification/core/`. Both tables and all section headings of the
result map must equal the versions generated from the map. The 38
negative controls must each be rejected with the expected diagnostic.
The checker validates the correspondence structure; it does not
compile Lean or prove the paper-only results.

## Markdown math

```sh
python3 tools/check_markdown_math.py
```

The command exited successfully with empty standard error:

```text
PASS: 22 tracked Markdown files; controls passed
```

The static guard checks the tracked Markdown files against the
documented GitHub math profile and exercises its own positive and
negative controls; the same result is obtained with `-O`. It does not
replace a live rendering check.

## Lean algebraic core

Lean is pinned to `v4.34.0-rc2` and Mathlib to
`85e3a25e006c35636f0e53b0e9296caca2685bc0`; all dependency revisions are
pinned in [lake-manifest.json](lean/lake-manifest.json). As in the
[Lean guide](lean/README.md), fetch the pinned dependencies and their
compiled cache from `lean/`, then run the verifier from the repository
root:

```sh
(cd lean && lake exe cache get)
python3 -B lean/verify
```

The result below is recorded from a separate build log of these
commands. The launcher ran the 17 source and execution controls under
normal and optimized Python and compared their diagnostics; the verifier
then cleaned this project, rebuilt all nine modules one by one, each
ending with `Build completed successfully`, and ran the axiom probes and
kernel controls. The result lines are:

```text
Ran 17 tests in <time>s
OK
PASS: pre-build audit controls agree under Python optimization
'TR29.univariate_moment_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.geometric_kernel_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.matrix_moment_leading' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.anti_diagonal_blocks' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.orthogonal_gram_assembly' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.tr29_gram_lower_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.finite_chart_avoidance' depends on axioms: [propext, Classical.choice, Quot.sound]
'TR29.core_theorems' depends on axioms: [propext, Classical.choice, Quot.sound]
ACCEPTED Positive
REJECTED WrongBound
REJECTED MissingMoments
REJECTED ZeroLeading
REJECTED WrongSign
REJECTED MissingOrthogonality
REJECTED WrongCount
REJECTED ZeroPolynomial
PASS: valid algebraic controls and seven intended mathematical rejections
PASS: rebuilt 9 proof modules; all project Lean sources checked.
PASS: complete source inventory and SHA256 binding match.
PASS: TR29.core_theorems and seven further probes use exactly propext, Classical.choice, Quot.sound.
```

The nine modules are `lean/TR29.lean` and the eight files in
`lean/TR29/`. The positive control covers empty matrices, blocks and
charts, zero and repeated nodes and the count 20 for the cubic triple;
the seven false controls must fail on their mathematical goals. Only
the three displayed axioms are permitted. The aggregate theorem states
neither rank formula; see the [formal scope](lean/SCOPE.md) and the
[result map](paper-lean-mapping/by-section.md) for the paper results it
supports.

## Manuscript

From `paper/`, with LaTeX, BibTeX and `latexmk` installed:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The build produced 16 pages. Its LaTeX log contained no warnings,
undefined references or citations, and no overfull boxes; four
underfull-box notices come from two bibliography entries with long URLs
(Behr and the TR-29 catalogue).
The included `paper/main.pdf` has SHA-256
`668d6d3cfa6790d3b2900ded04097b6400b58323811ee3071b361abad4eda482`.
The extracted text of the included and rebuilt PDFs is identical; its
SHA-256 under `pdftotext -layout` is
`f985897e25fa2b00bbbcbe7cffbebdab4e19493316903cee766c60a210757639`.
PDF container metadata may differ between builds.

## File integrity

From the repository root:

```sh
sha256sum --check SHA256SUMS
(cd paper && sha256sum --check SHA256SUMS)
(cd verification && sha256sum --check SHA256SUMS)
```

The root manifest lists every tracked file except itself. The paper
manifest lists every file in `paper/` except itself and the generated
`build/` directory: the README, licence, PDF, bibliography, the main
TeX file, the eight section files and the two appendix files. The
verification manifest lists the 24 other files in `verification/`, and
the nested manifests in `verification/core/verification/`
and `verification/core/families/monomial-products/verification/` are
enforced by the exact-check runners. Dependency caches and generated
build files are excluded. File hashes establish byte identity; the
commands above supply the verification evidence.
