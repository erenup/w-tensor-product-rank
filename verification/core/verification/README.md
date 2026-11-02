# Exact finite regressions

Run from this directory with Python 3.11 or later:

```sh
python3 -S -s -B run.py
```

Only the Python standard library is required. The two original scripts remain
unchanged, including the imported module name `exact_cyclotomic.py`.

`check_charts.py` checks rational univariate examples at degrees 2 through 9,
with chart parameter 2: prescribed moments, the anti-diagonal quantity, and
for degrees at least 3 the anti-triangular pattern and block rank. It also
checks one known 20-term cubic-triple decomposition over Q(zeta_10), in the
chart (2,3,4). The U Gram rank is 8, the three V Gram ranks are 4 each, the
distinct blocks are orthogonal, and the full Gram rank is 20.

`exact_cyclotomic.py` separately checks all 64 coefficients and 64 moments
of that fixed decomposition, four finite Hilbert ranks, and the intersection
and Gram ranks of the original symmetric-chart spaces. Arithmetic uses
`fractions.Fraction` and four rational coefficients modulo
X^4-X^3+X^2-X+1; there are no approximate rank decisions.

These finite regressions support the [written proof](../proofs/PROOF.md).
They do not prove its universal quantifiers, generic-parameter choice or
Laurent argument, and they do not verify every possible complex decomposition.
They give no border-rank or regrouped-mode rank conclusion.

## Controls and bindings

The chart script's three inline controls change a summand coefficient, choose
a chart pole, and incorrectly require the symmetric chart's V blocks to be
nondegenerate. The last control rejects that chart, not the valid decomposition.
The cyclotomic script's two inline controls omit a summand or change a summand
coefficient. [NEGATIVE_CONTROLS.json](NEGATIVE_CONTROLS.json) records all five
exact labels and rejection reasons. Their counts and definitions are mandatory.

[CHECKERS.txt](CHECKERS.txt) registers both executable scripts and their stdout
hashes. The runner executes each normally, under `-O`, and with a second hash
seed, requiring zero exit, empty stderr and byte-identical registered output.
It parses every output as strict JSON and checks all original control results
and the finite-case coverage. There are six script executions and 15 inline
control executions per complete runner call. Site initialization and bytecode
writes are disabled, and each script has a 120-second timeout.

[SHA256SUMS](SHA256SUMS) binds every verification file except itself. The runner
requires the exact file and script inventories, rejects symbolic links and
extra directories, and additionally binds the original script bytes to fixed
source hashes. Removing an inline control therefore fails even if the manifest
is recomputed. It rejects assertions, inexact literals, unsupported imports and
dynamic execution. JSON keys must be unique and numeric values integral.

[SOURCE_BINDINGS.txt](SOURCE_BINDINGS.txt) records the source and included
hashes of the two proof files. The runner checks source identifiers and the
complete two-file proof inventory. All file and proof hashes are checked again
after execution. Every failure exits nonzero, including under Python `-O`.

The main runner also invokes the
[binary-monomial product suite](../families/monomial-products/verification/README.md).
It requires that suite's directories and runner, rejects symbolic links and
propagates nonzero exit, stderr or timeout before reporting overall success.
The parent independently pins the child runner's exact bytes and stdout hash,
so replacing the child by an empty successful script also fails.
The child separately binds its exact checker, fixtures and three proof files,
and checks its eight original controls in all three modes.
