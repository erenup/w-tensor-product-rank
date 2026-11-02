# TR-29: universal algebraic core in Lean

`TR29.core_theorems : TR29.CoreTheorems` proves seven universally quantified
algebraic results used in the [rank proof](../verification/core/proofs/PROOF.md). The
[scope](SCOPE.md) lists the exact hypotheses and the remaining handwritten
steps. This is not a formalization of the full tensor-rank formula.

| Module | Result |
| --- | --- |
| `Univariate` | The moment bound n >= d-b+1 for arbitrary complex nodes and weights |
| `Series` | An actual geometric inverse, leading matrix coefficient and nonzero series determinant over every field |
| `Blocks` | Anti-diagonal block nonsingularity and orthogonal bilinear Gram independence |
| `Count` | The all-k count under explicit actual Gram hypotheses |
| `Avoidance` | A single finite chart avoiding every specified pole and nonzero polynomial |
| `Proofs` | Conjunction of the seven targets |

Zero and repeated nodes, signed weights, zero-sized matrices and zero-sized
blocks are covered as specified in [Statement.lean](TR29/Statement.lean).
The general matrix-series result uses coefficient fields of any characteristic.
No analytic convergence or numerical certificate is a premise.

The concrete multivariate U/V construction, the particular rational-to-series
and numerator identifications, the differential reduction from tensors, and
the cited upper bound remain in the written proof. The finite-character
upper construction for arbitrary binary-monomial products is also outside
this Lean core. The conditional Gram count must not be read as the full
moment-to-rank implication.

Lean is pinned to v4.34.0-rc2 and Mathlib to
85e3a25e006c35636f0e53b0e9296caca2685bc0. Install the toolchain specified
by `lean-toolchain` and make its `lake` command available. From this directory,
download the pinned dependencies and their compiled cache:

```sh
lake exe cache get
```

Then, from the repository root, run:

```sh
python3 -B lean/verify
```

The launcher runs the 17 source and execution audit controls in normal and
optimized Python, requires matching diagnostics after normalizing only the
reported test duration, and invokes the full Lean audit. It can also be run
as `python3 -B verify` from this directory.

The verifier checks the complete source and configuration bindings, cleans
only this project, rebuilds all nine modules serially with two Lean workers,
checks all eight exact target types and their transitive axioms, and runs one
positive regression file plus seven false mathematical controls. Allowed axioms
are exactly `propext`, `Classical.choice` and `Quot.sound`. Source and execution
mutation tests fail closed in normal and optimized Python.

The positive regressions include empty matrices/blocks/charts, zero/repeated
nodes and the count 20 for the cubic triple. False controls test an overstated
moment bound, missing upper-moment cancellation, a singular leading matrix,
the coefficient sign, missing Gram orthogonality, the all-k constant, and a
zero avoidance polynomial. They must fail on mathematical False goals, not
on missing imports or infrastructure errors.

The fresh-build audit removes this project's compiled modules before
rebuilding them. Compiled dependencies are retained; dependency downloads
are separate. Allow approximately 8 GiB of memory for the local audit.
