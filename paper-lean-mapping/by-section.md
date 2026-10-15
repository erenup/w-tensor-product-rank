# Paper results and their checks

The paper starts with the W-tensor upper bound and constructs the
matching lower bound through product moments and a weighted bilinear
Gram matrix. Its broader binary-monomial theorem is proved in full.
There are twelve numbered results, listed below. There are no numbered
definitions or remarks. The appendix is Section A.

| Result | Paper label | Coverage |
| --- | --- | --- |
| Theorem 1.1: binary-monomial rank formula | `thm:main` | Paper only; supporting components and examples are mapped separately |
| Corollary 1.2: products of W tensors | `cor:W` | Paper only; the formal W-block count is conditional |
| Theorem 2.1: product-moment lower bound | `thm:moment` | Paper only as a complete multivariate theorem |
| Lemma 2.2: basic Gram matrix | `lb:U-gram` | Specified finite supporting checks |
| Lemma 2.3: orthogonality of the lists | `lb:orthogonality` | Specified finite supporting checks |
| Lemma 2.4: first anti-diagonal block | `lb:anti-triangular` | Partial Lean coverage: conditional nonsingularity |
| Lemma 2.5: finite Laurent identity | `lb:Laurent` | Specified finite supporting checks |
| Lemma 2.6: nonzero rational determinant | `lb:H-nonsingular` | Partial Lean coverage: formal matrix-moment mechanism |
| Proposition 3.1: tensor-to-moment lower bound | `prop:lower` | Paper only |
| Lemma 4.1: lattice index and box avoidance | `ub:lattice` | Eight finite supporting examples |
| Lemma 4.2: character orthogonality | `ub:orthogonality` | Finite sums used in those examples |
| Proposition 4.3: character upper decomposition | `prop:upper` | Explicit finite identities; the universal construction is paper only |

## 1. Rank, the main result, and its context

Theorem 1.1 proves the fixed-block complex rank formula for every
$k\geq1$ and $a_i\geq b_i\geq1$. Corollary 1.2 specializes it to
products of generalized W tensors with $k\geq2$ and $d_i\geq3$.
Neither complete tensor statement is a Lean theorem.

The target `TR29.tr29_gram_lower_bound` in
[Count.lean](../lean/TR29/Count.lean) is a conditional part of the lower
argument. For $k\geq1$ and $d_i\geq2$, it assumes literal zero
cross-block pairings and nonsingular within-block Gram matrices of sizes
$2^k$ and $(d_i-2)2^{k-1}$. It then derives

```math
n\geq2^{k-1}\left(\sum_i d_i-2k+2\right).
```

The hypotheses are essential to the formal target. It does not
construct the vectors or prove their Gram properties from product
moments. It does not state the full binary-monomial count.

`exact_cyclotomic.py:main` checks all 64 coefficients and 64 moments of
one 20-term cubic-W triple decomposition, four finite Hilbert ranks and
the symmetric-chart intersection calculations. The function
`check_charts.py:cubic_chart` checks a nonsingular Gram construction for
that identity at parameters `(2,3,4)`. These are checks of the specified
identity and chart, not a lower bound for all possible decompositions.

## 2. A product-moment lower bound

Theorem 2.1 starts with moments on the entire coordinate degree box,
with nonzero degree-$b_i$ moments and vanishing subsequent moments up to
$d_i$. It assumes $b_i\geq1$ and $d_i\geq2b_i$. Nodes may repeat and
their coordinates may vanish; no positivity is assumed. The complete
theorem, including construction and verification of its specific
multivariate vectors, is paper only.

### One-coordinate support

`TR29.univariate_moment_bound` in
[Univariate.lean](../lean/TR29/Univariate.lean) proves a universal
one-coordinate statement: a nonzero degree-$b$ moment and zero moments
above it through degree $d$ imply $n\geq d-b+1$, for $b\geq1$ and
$d\geq b$. It permits arbitrary complex weights and zero or repeated
nodes. This is a supporting result, not a formalization of the full
multivariate theorem or a replacement for a numbered paper lemma.

`check_charts.py:univariate_cases` checks rational examples in degrees
2 through 9 at parameter 2, including the anti-diagonal value and, where
present, the extra-block zero pattern and rank.

### The basic block and cross-block cancellation

Lemma 2.2 identifies the Gram matrix of $\mathcal U$ as a Kronecker
product and proves the exact nonzero constant determinant of each
factor. Lemma 2.3 verifies every cross-block cancellation inside the
moment degree box. These symbolic multivariate claims are paper only.
The concrete finite examples check their corresponding evaluated
matrices and zero pairings.

`TR29.orthogonal_gram_assembly` in
[Blocks.lean](../lean/TR29/Blocks.lean) proves the general final linear
algebra step: for actual vectors and a weighted bilinear pairing, zero
cross-block pairings and nonzero within-block Gram determinants imply
independence of the concatenated family and the sum-of-sizes dimension
bound. Orthogonality and local nondegeneracy are explicit hypotheses.
The formal theorem does not prove Lemma 2.3 for the paper's vectors.

### Extra-block nondegeneracy

Lemma 2.4 gives an exact signed determinant-power formula after reversing
block columns. `TR29.anti_diagonal_blocks` in
[Blocks.lean](../lean/TR29/Blocks.lean) proves its general nonsingularity
mechanism: an actual matrix with the required zero blocks and a common
nonsingular block on the first anti-diagonal has nonzero determinant.
The remaining blocks are unrestricted and zero-sized blocks are allowed.
The specific moment cancellations, index shift and exact signed
determinant formula remain in the paper.

Lemma 2.5 proves the finite Laurent identity and its remainder statement,
including zero nodes without division by a node coordinate. Selected
rational instances are checked by `check_exact.py:lower`. The universal
finite identity itself is paper only.

Lemma 2.6 proves that each particular rational matrix $H_i$ has nonzero
determinant. Two targets in [Series.lean](../lean/TR29/Series.lean)
support its formal-series mechanism:

| Declaration | Exact formal content |
| --- | --- |
| `TR29.geometric_kernel_identity` | The actual geometric kernel is an inverse of the corresponding linear power series over any field of the stated Lean type |
| `TR29.matrix_moment_leading` | Actual matrix-moment hypotheses give zero lower coefficients, a prescribed first coefficient and a nonzero determinant of the actual moment-series matrix |

The second target uses a nonsingular degree-$b$ matrix moment,
vanishing moments above it through $d$, $b\geq1$ and $d\geq b$.
It applies over rational-function coefficient fields in the other
parameters. Its determinant conclusion is derived, not assumed.
At a zero node, the positive node power annihilates the contribution.

The identification of each specific rational $H_i$ with this formal
series, verification of its matrix-moment hypotheses, transfer back
to the rational determinant and construction of its nonzero numerator
polynomial remain in the paper. Formal nonvanishing must not be
reported as an automatic proof of that entire connection.

### One common finite choice and the count

`TR29.finite_chart_avoidance` in
[Avoidance.lean](../lean/TR29/Avoidance.lean) proves simultaneous
avoidance of every coordinate pole and a finite list of nonzero
multivariate polynomials. It produces one finite complex tuple.
Its premise already requires every input polynomial to be nonzero;
it does not supply the preceding numerator argument.

In the concluding proof of Theorem 2.1, the paper clears the specific
denominators, verifies nonzero numerators, chooses a common finite
point, assembles the particular Gram matrix and counts

```math
Q+\sum_i(d_i-2b_i)\frac{Q}{b_i+1},
\qquad Q=\prod_i(b_i+1).
```

This complete binary-monomial count and its application to the
constructed vectors are paper only. The formal numerical target uses
the W-block sizes described in Section 1.

## 3. From decompositions to product moments

Proposition 3.1 starts with an arbitrary finite fixed-block complex
decomposition. The affine chart, absorption of scales into nonzero
weights, differential-operator coefficient calculation and nonzero
top moments are paper only. The coefficient box and polynomial
functional are exact; no moments outside the box are assumed.

The initial affine normalization and the later Gram-parameter choice
have different purposes. Both are chosen after fixing the decomposition.
Neither is a genericity assumption on its support. The supplied Lean
targets do not formalize this tensor coordinate reduction.

## 4. A finite-character decomposition

Lemma 4.1 proves the determinant and index of the column lattice and
its avoidance of the coefficient box. Lemma 4.2 proves the general
finite-character count and orthogonality formula. Proposition 4.3 uses
both to verify every coefficient of the universal upper identity,
including its nonzero weights and exact summand count. All these
universal claims remain in the paper.

`families/monomial-products/verification/check_exact.py:upper` checks
eight explicit exponent tuples, whose summand counts are 54, 64, 51,
20, 66, 15, 8 and 24 in [fixture order](../families/monomial-products/verification/fixtures.json).
It checks integer determinants and lattice membership and reduces each
coefficient sum exactly modulo a cyclotomic polynomial. The examples
include unequal exponents, balanced factors, four blocks, and the
one-block, two-block and cubic-W specializations. These examples do not
prove the lattice or character theorem for all parameters.

## 5. Specializations and scope

The one-block and two-block formulas, balanced case, cubic-W rank 20
and rank 54 of the triple product of $x^3y^2$ follow from the complete
paper theorem. The theorem excludes $b_i=0$. The Gram form is bilinear
over the complex numbers; no positivity or Hermitian argument is used.
Formal-series reasoning certifies nonzero rational functions before a
single finite evaluation. It does not introduce a border-rank or
limiting-decomposition conclusion.

## A. Exact finite checks

The root suite checks the specified W identities and finite charts.
The binary-monomial suite additionally checks three rational cubatures
with Gram-list lengths 33, 54 and 13. Those calculations include zero
coordinates and repeated nodes, verify the complete moment boxes,
evaluate all Gram entries and a nonzero full determinant, and test
the finite Laurent identity at selected zero, positive and negative
nodes. Both suites use exact arithmetic and negative controls.

The seven formal targets and `TR29.core_theorems` are separately
checked by the Lean audit's exact-type and axiom probes. The mapping
checker verifies that these references and all twelve numbered paper
results exist. It does not compile Lean or replace the mathematical
checks. See [the Lean guide](../lean/README.md) and
[verification guide](../verification/README.md) for their commands.
