# From moment conditions to a rank bound

For products of generalized W-states with fixed symmetric blocks, the
known upper bound is

```math
M=2^{k-1}\left(\sum_{i=1}^k d_i-2k+2\right),
\qquad k\geq2,\quad d_i\geq3.
```

The lower-bound question is whether every decomposition needs at least
$M$ summands. The [paper](../paper/main.pdf) answers it in Theorem 1.1,
and Section 8 proves the broader formula for products of binary
monomials. This guide follows the moment and Gram-matrix argument, then
identifies which parts have formal or finite exact checks.

## Normalize a decomposition and match its coefficients

Start with an arbitrary decomposition of $`\prod_i x_i^{d_i-1}y_i`$ into
products of $`d_i`$th powers of complex linear forms, with the
symmetric blocks fixed (Definition 1.1). Delete zero summands, and let
$r$ be the number remaining. Lemma 2.1 chooses an invertible
coordinate change so that all remaining factors have an affine
normalization. The scales become nonzero weights $`w_\ell`$, and the
normalized coefficients become points $`z_\ell\in\mathbb C^k`$. Points
may repeat and their coordinates may vanish. This normalization imposes
no restriction on the original decomposition.

Matching every coefficient gives the product-moment identities of
Lemma 3.1,

```math
\sum_{\ell=1}^r w_\ell\prod_{i=1}^k z_{i\ell}^{e_i}
 =\prod_{i=1}^k m_i(e_i),
\qquad 0\leq e_i\leq d_i,
```

with $`m_i(0)=\gamma_i`$, $`m_i(1)=\beta_i=1/d_i`$ and $`m_i(e)=0`$ for
$`2\leq e\leq d_i`$. By linearity (Lemma 4.1), these identities
determine a functional on the polynomials whose degree in each
coordinate $`Z_i`$ is at most $`d_i`$. They do not prescribe values
outside that box. For the binary-monomial theorem of Section 8, the
coordinate moments vanish in degrees $`b_i+1,\ldots,d_i`$, while
$`\beta_i=m_i(b_i)`$ is nonzero; there $`b_i\geq1`$ and
$`d_i\geq2b_i`$.

## Build the weighted Gram matrix

Introduce auxiliary parameters $`t_i`$ with $`1+t_iz_{i\ell}\neq0`$,
the polynomial $`H_t(Z)=\prod_i(1+t_iZ_i)^{d_i}`$, and $M$ rational test
functions $`\phi_a`$. Their evaluations at the points are the columns
of an $r$-by-$M$ matrix $E$. With $W$ the diagonal matrix of the
weights $`w_\ell H_t(z_\ell)`$, Lemma 5.1 gives

```math
\mathcal G=E^{\mathsf T}WE.
```

This is a complex symmetric bilinear matrix, with no conjugation and no
positivity assumption. Lemma 6.1 shows that invertibility of
$`\mathcal G`$ forces the $M$ columns of $E$ to be independent, so
$r\geq M$.

Section 7 fixes the functions: a basic family $`\mathcal B_0`$ of
$`2^k`$ functions and, for each block, an additional family
$`\mathcal B_i`$ of $`(d_i-2)2^{k-1}`$ functions. Moment cancellation
makes different families orthogonal (Lemma 7.1 and Appendix A). That
alone does not imply independence: each diagonal Gram block must also
be nonsingular. The basic block is a Kronecker product of $2\times2$
matrices with determinant $`-\beta_i^2`$. Reversing the block columns
of an additional family gives a block triangular matrix whose diagonal
blocks are $`H_i(t)`$ (Lemma 7.2). Exact Laurent coefficients show that
each $`\det H_i`$ is a nonzero rational function (Lemma 7.3 and
Appendix B). After clearing denominators, one finite parameter vector
avoids every determinant zero and every pole simultaneously
(Proposition 7.1). Separate parameter choices for different blocks
would not suffice.

At this common finite point $`\mathcal G`$ is invertible, so $r\geq M$.
The cited upper bound then gives Theorem 1.1. No limiting decomposition
is used.

## The binary-monomial extension

For every $k\geq1$ and $`a_i\geq b_i\geq1`$, with $`d_i=a_i+b_i`$,
Theorem 8.1 gives the fixed-block complex rank

```math
N=\prod_i(b_i+1)
  +\sum_i(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

Theorem 8.2 proves the lower bound for abstract product moments, with a
basic list of $`\prod_i(b_i+1)`$ functions and lists $`\mathscr V_i`$ of
$`(d_i-2b_i)\prod_{j\neq i}(b_j+1)`$ functions; balanced factors have
empty additional lists. Proposition 8.1 reduces an arbitrary
decomposition to those moments by differential operators. A lattice of
index $N$ avoiding the coefficient box and character orthogonality on
the quotient (Lemmas 8.6 and 8.7) give the matching explicit
decomposition of Proposition 8.2. The W case is $`b_i=1`$
(Remark 8.1), where Proposition 8.2 also gives an $M$-term
decomposition.

All statements concern exact complex rank with the displayed symmetric
blocks fixed. The paper does not identify this rank with real, border,
cactus or unrestricted nonsymmetric rank, or with rank after grouping
modes from different blocks. Pure-power factors $`b_i=0`$ are excluded
(Remark 8.2).

## Read the evidence at the right level

[by-section.md](by-section.md) maps all 31 numbered results of the
paper, including the examples, remarks and the appendix lemma.
[mapping.json](mapping.json) records the exact source labels,
declarations, check functions and coverage boundaries.

The [Lean core](../lean/README.md) proves seven universal algebraic
targets: a one-coordinate moment lower bound, a geometric-series
inverse identity, a matrix-moment leading-coefficient theorem,
anti-diagonal block nonsingularity, orthogonal Gram assembly, the
conditional W-block count, and simultaneous finite chart avoidance.
Their conjunction is `TR29.core_theorems`. The one-coordinate bound is
the case $k=1$ of Theorem 8.2, and the one-block Gram assembly is the
implication of Lemma 6.1.

The specific multivariate test functions and their cancellations are
paper only. So are the identification of each rational $`H_i`$ with its
formal series, the nonzero determinant numerators, the reduction of an
arbitrary decomposition to moments, the general binary count, and the
lattice and character construction. The chart theorem starts with
polynomials already known to be nonzero; the Gram theorems start with
explicit orthogonality and determinant hypotheses. No Lean theorem
states either rank formula.

The [exact checks](../verification/README.md) verify specified
rational and cyclotomic examples: all coefficients and moments of one
20-term decomposition of the cubic triple and its nonsingular
$`20\times20`$ Gram matrix, one-coordinate block patterns, all
coefficients of eight character identities, and three full Gram
calculations with repeated and zero-coordinate points. These finite
checks support the formulas; they do not establish universal
quantifiers by enumeration. A nonsingular Gram matrix for one chosen
decomposition does not by itself prove a lower bound for every
decomposition.

## Check the correspondence

From the repository root, run:

```sh
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
```

The standard-library checker reconstructs the paper title, subtitle and
authors, the numbered sections and appendices, and every numbered
result with its own per-section counter, and requires an exact mapping
entry for each. It checks labels and source locations, result names,
Lean theorem names and their proposition types, all eight exact-type
probes and axiom requests in `lean/audit/Axioms.lean`, and each mapped
Python function under `verification/core/`. Both tables and all section
headings of [by-section.md](by-section.md) must equal the versions
generated from the map. A comment cannot supply a missing declaration
or probe.

Thirty-eight in-memory negative controls exercise missing, duplicate
and unmapped results, changed numbering and counters, a missing
appendix transition, stale titles, authors, sections and inputs,
altered Lean theorems and audit probes, misplaced exact checks,
unsupported coverage claims and stale result tables. Both commands
produce identical output. This checks the source correspondence; it
neither compiles Lean nor executes the mathematical examples. Use the
separate [Lean commands](../lean/README.md) and
[exact-check commands](../verification/README.md) for those tasks.
