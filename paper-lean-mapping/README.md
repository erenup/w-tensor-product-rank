# From moment conditions to a rank bound

For products of generalized W tensors with fixed symmetric blocks, the
known upper bound is

```math
M=2^{k-1}\left(\sum_{i=1}^k d_i-2k+2\right),
\qquad k\geq2,\quad d_i\geq3.
```

The lower-bound question is whether every decomposition needs at least
$M$ summands. The [paper](../paper/main.pdf) answers it and proves the
broader formula for products of binary monomials. This guide follows
the moment and Gram-matrix argument, then identifies which parts have
formal or finite exact checks.

## Normalize a decomposition and match its coefficients

Start with an arbitrary decomposition into products of powers of complex
linear forms, with the symmetric blocks fixed. Delete zero summands,
and let $r$ be the number remaining. Choose an invertible coordinate
change so that all remaining factors
have an affine normalization. The scales become nonzero weights
$`w_\ell`$, and the normalized coefficients become nodes
$`z_\ell\in\mathbb C^k`$. Nodes may repeat and their coordinates may
vanish. This normalization imposes no restriction on the original
decomposition.

Matching every coefficient gives the product-moment identities

```math
\sum_{\ell=1}^r w_\ell\prod_{i=1}^k z_{i,\ell}^{e_i}
 =\prod_{i=1}^k m_i(z_i^{e_i}),
\qquad 0\leq e_i\leq d_i.
```

By linearity, these identities describe a polynomial functional on
the space whose degree in each coordinate $`z_i`$ is at most $`d_i`$.
They do not prescribe moments outside that box. For the general
binary-monomial theorem, the coordinate moments vanish above degree
$`b_i`$, while $`m_i(z_i^{b_i})`$ is nonzero. The assumptions are
$`b_i\geq1`$ and $`d_i\geq2b_i`$.

## Build the weighted Gram matrix

Introduce auxiliary parameters $`t_i`$ and the diagonal bilinear weights

```math
w_\ell(t)=w_\ell\prod_i(1+t_i z_{i,\ell})^{d_i}.
```

The paper's evaluation lists $`\mathcal U,\mathcal V_1,\ldots,
\mathcal V_k`$ are the batches $`\mathcal B_0,\mathcal B_1,\ldots,
\mathcal B_k`$ in the introductory Gram-matrix description. In the
W case they contain $M$ functions altogether. Their evaluations are
the columns of an $r$-by-$M$ matrix $E$. With $W$ the diagonal matrix
of the weights above, their combined Gram matrix is

```math
G=E^{\mathsf T}WE.
```

This is a complex symmetric bilinear matrix, with no conjugation,
positive weights or positivity assumption. Moment cancellation makes
different batches orthogonal. That alone does not imply independence:
each diagonal Gram block must also be nonsingular.

The basic block has an explicit nonzero determinant. Reversing the
block columns of an additional batch gives a triangular matrix whose
diagonal blocks are $`H_i`$. Exact Laurent coefficients show that each
$`\det H_i`$ is a nonzero rational function. After clearing denominators,
one finite parameter vector avoids every determinant zero and every
pole simultaneously. Separate parameter choices for different blocks
would not suffice.

At this common finite point, $G$ is invertible, so the columns of $E$
are independent and $r\geq M$. The known upper bound then gives the
W-tensor equality. No limiting decomposition is used.

## The binary-monomial extension

The paper proves the more general theorem. For every $k\geq1$ and
$`a_i\geq b_i\geq1`$, with $`d_i=a_i+b_i`$, the fixed-block complex rank is

```math
N=\prod_i(b_i+1)
  +\sum_i(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

The same moment argument uses $`Q=\prod_i(b_i+1)`$ basic functions and
$`(d_i-2b_i)Q/(b_i+1)`$ functions in batch $i$. Balanced factors have
empty additional batches. A finite-character construction supplies
the matching general upper bound. The W specialization is $`b_i=1`$;
the Lean numerical target specifically covers that block count.

All statements concern exact complex rank with the displayed symmetric
blocks fixed. The proof does not identify this rank with real, border,
cactus or unrestricted nonsymmetric rank, or rank after grouping
different original blocks. SOS decompositions permit
different terms and are a separate decomposition problem.

## Read the evidence at the right level

[by-section.md](by-section.md) maps every numbered paper result.
[mapping.json](mapping.json) records the exact source labels,
declarations, check functions and coverage boundaries.

The [Lean core](../lean/README.md) proves seven universal algebraic
targets: a one-coordinate moment lower bound, a geometric-series
inverse identity, a matrix-moment leading-coefficient theorem,
anti-diagonal block nonsingularity, orthogonal Gram assembly, the
conditional W-block numerical count, and simultaneous finite chart
avoidance. Their conjunction is `TR29.core_theorems`.

The specific multivariate evaluation vectors and their cancellations
are paper only. So are the identification of each rational $`H_i`$ with
its formal series, the nonzero determinant-numerator bridge, reduction
of an arbitrary tensor decomposition to moments, the full binary count,
and the general finite-character upper construction. The chart theorem
starts with polynomials already known to be nonzero; the Gram assembly
theorems start with explicit orthogonality and determinant hypotheses.
No Lean theorem states the full multivariate moment or tensor-rank
formula.

The [exact-check suite](../verification/README.md) verifies specified
rational and cyclotomic examples. The
[binary-monomial checks](../families/monomial-products/verification/README.md)
include all coefficients of eight character identities and three full
Gram calculations with repeated and zero-coordinate nodes. These finite
checks support the formulas; they do not establish universal quantifiers
by enumeration. A full-rank Gram matrix for one chosen decomposition
does not by itself prove a lower bound for every decomposition.

## Check the correspondence

From the repository root, run:

```sh
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
```

The standard-library checker reconstructs the numbered-result inventory,
including the appendix transition, and requires every result to have a
direct label and an exact mapping entry. It checks source locations,
Lean theorem names and named proposition types, all eight exact-type
probes and axiom requests in `lean/audit/Axioms.lean`, and each mapped
Python function. A comment cannot supply a missing declaration or probe.

Twenty in-memory negative controls exercise missing and duplicate
references, changed numbering, altered theorem types, missing audit
probes and unsupported coverage claims. Both commands produce identical
output. This checks the source correspondence; it neither compiles Lean
nor executes the mathematical examples. Use the separate
[Lean commands](../lean/README.md) and
[exact-check commands](../verification/README.md) for those tasks.
