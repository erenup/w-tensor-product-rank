# Exact verification

Run from the repository root with Python 3.11 or later:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
```

[run.py](run.py) authenticates every file in this directory against
[SHA256SUMS](SHA256SUMS), binds the child runner and its manifest by digest,
runs the child in normal, optimized and alternate hash-seed modes, requires
the recorded output in each mode, and rejects altered inventories.

- [core/proofs/](core/proofs/): the plain-text statement and proof of the W-product rank.
- [core/verification/](core/verification/): exact checks for the W-product lower bound; its
  runner also executes the binary-monomial suite. See its [guide](core/verification/README.md).
- [core/families/monomial-products/](core/families/monomial-products/): the plain-text
  statement, proof and literature notes for products of binary monomials, with their
  exact checks.

These finite checks support the written proofs; they do not replace any
all-parameter statement. The [review record](reviews/README.md) collects the
independent audits of the paper's mathematics.
