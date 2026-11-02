# Paper results and their checks

The numbering below is read from [the paper source](../paper/main.tex)
of *The Exact Partially Symmetric Rank of Products of W-States*. The
paper has eight numbered sections and two appendices, A and B, and 31
numbered results: three theorems, three propositions, sixteen lemmas,
one definition, six examples and two remarks. There are no corollaries.
Each kind of result has its own counter within each section, so for
instance Lemma 7.1, Proposition 7.1 and Example 7.1 are different
results. Definition 1.1 has no label. The unnumbered Statements and
Declarations contain no mathematical result. Both tables are generated
from [mapping.json](mapping.json) and must agree with it exactly;
[build_and_check.py](build_and_check.py) verifies this.

| Paper result | Label | Coverage |
| --- | --- | --- |
| Definition 1.1: Partially symmetric rank | none | Paper only |
| Theorem 1.1: Exact partially symmetric rank | `thm:main` | Partial Lean coverage: `TR29.tr29_gram_lower_bound` |
| Example 1.1: Three cubic factors | `ex:rank20` | Paper proof; finite exact checks: `exact_cyclotomic.py:main`, `check_charts.py:cubic_chart` |
| Lemma 2.1: Affine normalization | `lem:coordinates` | Paper only |
| Lemma 3.1: Moment conditions | `lem:moments` | Paper proof; finite exact checks: `exact_cyclotomic.py:main` |
| Lemma 4.1: Generalized moment conditions | `lem:generalized` | Paper only |
| Lemma 5.1: Gram factorization | `lem:gram` | Paper only |
| Lemma 6.1: The dimension bound | `lem:dimension` | Partial Lean coverage: `TR29.orthogonal_gram_assembly` |
| Example 7.1: The twenty functions for three cubic factors | `ex:list` | Paper proof; finite exact checks: `check_charts.py:cubic_chart` |
| Lemma 7.1: Block diagonal structure | `lem:blocks` | Paper proof; finite exact checks: `check_charts.py:cubic_chart` |
| Example 7.2: An explicit basic Gram block | `ex:G0` | Paper only |
| Lemma 7.2: The anti-triangular blocks | `lem:anti` | Partial Lean coverage: `TR29.anti_diagonal_blocks`; finite exact checks: `check_charts.py:univariate_cases` |
| Example 7.3: Column reversal when $`d_i=5`$ | `ex:reversal` | Paper only |
| Lemma 7.3: Nonzero determinant of each additional block | `lem:Hi` | Partial Lean coverage: `TR29.geometric_kernel_identity`, `TR29.matrix_moment_leading`; finite exact checks: `check_charts.py:univariate_cases` |
| Proposition 7.1: Simultaneous Gram nondegeneracy | `prop:nondegenerate` | Partial Lean coverage: `TR29.finite_chart_avoidance`; finite exact checks: `check_charts.py:cubic_chart` |
| Example 7.4: The $`20\times20`$ Gram matrix | `ex:twenty` | Paper proof; finite exact checks: `check_charts.py:cubic_chart` |
| Theorem 8.1: Products of binary monomials | `thm:binary` | Paper proof; finite exact checks: `check_exact.py:upper` |
| Theorem 8.2: Product-moment lower bound | `thm:pm` | Partial Lean coverage: `TR29.univariate_moment_bound`, `TR29.orthogonal_gram_assembly`, `TR29.finite_chart_avoidance`; finite exact checks: `check_exact.py:lower` |
| Lemma 8.1: The basic block | `lem:bm-basic` | Paper proof; finite exact checks: `check_exact.py:lower` |
| Lemma 8.2: Orthogonality of the lists | `lem:bm-orth` | Paper proof; finite exact checks: `check_exact.py:lower` |
| Lemma 8.3: The anti-triangular blocks | `lem:bm-anti` | Partial Lean coverage: `TR29.anti_diagonal_blocks`; finite exact checks: `check_exact.py:lower` |
| Lemma 8.4: A finite division identity | `lem:bm-division` | Paper proof; finite exact checks: `check_exact.py:lower` |
| Lemma 8.5: Nonsingularity of the additional blocks | `lem:bm-Hi` | Partial Lean coverage: `TR29.geometric_kernel_identity`, `TR29.matrix_moment_leading` |
| Proposition 8.1: Reduction to moments | `prop:bm-reduction` | Paper only |
| Lemma 8.6: A lattice avoiding the coefficient box | `lem:bm-lattice` | Paper proof; finite exact checks: `check_exact.py:upper` |
| Lemma 8.7: Finite character orthogonality | `lem:bm-characters` | Paper proof; finite exact checks: `check_exact.py:upper` |
| Proposition 8.2: An explicit decomposition | `prop:bm-upper` | Paper proof; finite exact checks: `check_exact.py:upper` |
| Remark 8.1: The case $`b_i=1`$ | `rem:bm-W` | Paper proof; finite exact checks: `check_exact.py:upper` |
| Example 8.1: Ranks $`20`$ and $`54`$ | `ex:bm-54` | Paper proof; finite exact checks: `check_exact.py:upper`, `check_exact.py:lower` |
| Remark 8.2: Pure-power factors | `rem:bm-pure` | Paper only |
| Lemma B.1: Finite division identity | `lem:division` | Paper proof; finite exact checks: `check_exact.py:lower` |

"Paper only" means that no Lean declaration or exact check is assigned
to the result. A Lean entry proves only the scope stated in the section
below; no rank formula is a Lean theorem. Finite exact checks test
specified cases and do not prove a universal statement. All checks
named here live under `verification/core/`: `check_charts.py` and
`exact_cyclotomic.py` in `verification/core/verification/`, and
`check_exact.py` in `verification/core/families/monomial-products/verification/`.

The Lean targets and exact checks enter the proofs at the following
equation anchors:

| Supporting anchor | Section | Lean targets | Exact checks |
| --- | --- | --- | --- |
| `eq:upper`: Cited upper bound | 1 | None | `exact_cyclotomic.py:main` |
| `eq:moments`: Moment conditions on the full box | 3 | None | `exact_cyclotomic.py:main` |
| `eq:Mcount`: Length of the test-function list | 7 | `TR29.tr29_gram_lower_bound` | None |
| `eq:det-block`: Determinant of an additional Gram block | 7 | `TR29.anti_diagonal_blocks` | `check_charts.py:univariate_cases` |
| `eq:laurent`: Leading Laurent coefficient of $`H_i`$ | 7 | `TR29.geometric_kernel_identity`, `TR29.matrix_moment_leading` | None |
| `eq:avoidance`: Avoidance polynomial for the W lists | 7 | `TR29.finite_chart_avoidance` | None |
| `eq:twenty`: The $`20\times20`$ Gram matrix | 7 | None | `check_charts.py:cubic_chart` |
| `eq:bm-leading`: Leading Laurent coefficient for general $`b_i`$ | 8 | `TR29.matrix_moment_leading` | None |
| `eq:bm-avoidance`: Avoidance polynomial and final count | 8 | `TR29.finite_chart_avoidance`, `TR29.orthogonal_gram_assembly` | `check_exact.py:lower` |
| `eq:bm-division`: Finite division identity | 8 | None | `check_exact.py:lower` |
| `eq:bm-box`: Lattice avoids the coefficient box | 8 | None | `check_exact.py:upper` |
| `eq:bm-character`: Character decomposition | 8 | None | `check_exact.py:upper` |
| `eq:division`: Division identity for $`b=1`$ | B | None | `check_exact.py:lower` |
| `eq:det-laurent`: Leading determinant of $`H_i`$ | B | `TR29.matrix_moment_leading` | None |

## 1. Introduction and main result

Definition 1.1 fixes the partially symmetric rank: the $k$ binary
blocks $`(x_i,y_i)`$ and their degrees $`d_i`$ stay fixed, and the
summands are products of $`d_i`$th powers of complex linear forms in the
blocks. Theorem 1.1 states, for $k\geq2$ and $`d_i\geq3`$, that the rank
of $`\prod_i x_i^{d_i-1}y_i`$ is
$`M=2^{k-1}(\sum_i d_i-2k+2)`$. The upper bound at `eq:upper` is cited
from Canino, Casarotti and Santarsiero; Proposition 8.2 gives an
explicit $M$-term decomposition as well (Remark 8.1). The lower bound
is proved in Sections 2 to 7 and completed at the end of Section 7,
where the paper notes that it holds for all $k\geq1$ and $`d_i\geq2`$.
Neither the theorem nor its lower bound is a Lean theorem.

`TR29.tr29_gram_lower_bound` in [Count.lean](../lean/TR29/Count.lean)
is the counting step. For $k\geq1$ and $`d_i\geq2`$ it assumes literal
zero cross-block pairings and nonsingular within-block Gram matrices of
sizes $`2^k`$ and $`(d_i-2)2^{k-1}`$, and derives $n\geq M$. It does not
construct the test functions or prove their Gram properties.

For Example 1.1, `exact_cyclotomic.py:main` checks all 64 coefficients
of one 20-term decomposition of the cubic triple over
$`\mathbb Q(\zeta_{10})`$, and `check_charts.py:cubic_chart` checks a
nonsingular evaluated $`20\times20`$ Gram matrix for it. These show that
20 terms suffice for this target and exhibit the lower-bound mechanism
for one decomposition; they do not show that fewer terms are impossible.

## 2. A change of coordinates

Lemma 2.1 chooses $`\gamma_i`$ outside finitely many values and rewrites
every nonzero summand as a weight $`w_\ell\neq0`$ times
$`\prod_i(X_i+z_{i\ell}Y_i)^{d_i}`$. Repeated points and zero coordinates
are allowed. The lemma is paper only.

## 3. Coefficient matching and moment conditions

Lemma 3.1 shows that the normalized identity is equivalent to the
product moment conditions on the full box $`0\leq e_i\leq d_i`$, with
$`m_i(0)=\gamma_i`$, $`m_i(1)=\beta_i=1/d_i`$ and $`m_i(e)=0`$ for
$`2\leq e\leq d_i`$. The weights are complex and need not be positive.
For the one 20-term decomposition above, `exact_cyclotomic.py:main`
checks both its coefficients and the 64 moments of its normalized nodes
and weights, with $`\gamma_i=0`$ and $`\beta_i=1/3`$. The equivalence
for every decomposition is paper only.

## 4. Generalized moment conditions

Lemma 4.1 extends the moment conditions by linearity to every
polynomial of degree at most $`d_i`$ in each $`Z_i`$, with the product
rule for products of univariate factors. It is paper only. The section
notes that the formula does not apply directly to rational functions;
the entries treated in Lemma 7.3 and Appendix B are handled separately.

## 5. Constructing the weighted Gram matrix

Lemma 5.1 writes the Gram matrix of the evaluation vectors as
$`E^{\mathsf T}WE`$, with $W$ diagonal and complex. It is paper only.
The Lean definition `TR29.weightedGram` in
[Definitions.lean](../lean/TR29/Definitions.lean) uses the same
bilinear pairing $`\sum_\ell w_\ell u_\ell v_\ell`$, without
conjugation, in all Gram targets below.

## 6. From Gram invertibility to a rank lower bound

Lemma 6.1 states that an invertible Gram matrix forces the $M$ columns
of $E$ to be independent, so $r\geq M$. The one-block case of
`TR29.orthogonal_gram_assembly` in [Blocks.lean](../lean/TR29/Blocks.lean)
is this implication for arbitrary complex vectors and weights. With
several blocks the same target also gives the final assembly used in
Proposition 7.1 and in the proof of Theorem 8.2: zero cross-block
pairings and nonzero within-block Gram determinants imply independence
of the whole family and the sum-of-sizes bound. Orthogonality and the
block determinants are explicit hypotheses of the target.

## 7. A specific family of test functions

The section defines the basic family $`\mathcal B_0`$ and the additional
families $`\mathcal B_i`$, counts $M$ functions at `eq:Mcount`, and
proves invertibility of their Gram matrix at one finite parameter.

Lemma 7.1 proves the block-diagonal form, the Kronecker formula for the
basic block and $`\det G_i=-\beta_i^2`$; the cross-block cancellations
are recorded in Appendix A. These multivariate claims are paper only.
`check_charts.py:cubic_chart` checks the zero cross blocks and the basic
Gram rank 8 for one decomposition of the cubic triple at $t=(2,3,4)$.

Lemma 7.2 proves the anti-triangular block pattern and
$`\det\mathcal G_i=\pm\det H_i^{d_i-2}`$. `TR29.anti_diagonal_blocks`
in [Blocks.lean](../lean/TR29/Blocks.lean) proves the nonsingularity
mechanism: a block matrix with zero blocks above the first anti-diagonal
and one nonsingular block repeated on it has nonzero determinant, after
shifting $`s=2,\ldots,d_i-1`$ to $`0,\ldots,d_i-3`$. The moment
cancellations and the signed power formula remain in the paper.
`check_charts.py:univariate_cases` checks the pattern and block rank
$d-2$ in one coordinate for $d=3,\ldots,9$.

Lemma 7.3 proves that each $`\det H_i`$ is a nonzero rational function
through the leading Laurent coefficient at `eq:laurent`. Two targets in
[Series.lean](../lean/TR29/Series.lean) supply its formal mechanism:

| Declaration | Exact formal content |
| --- | --- |
| `TR29.geometric_kernel_identity` | The geometric kernel is an inverse of the corresponding linear power series over every field of the stated Lean type |
| `TR29.matrix_moment_leading` | Matrix-moment hypotheses give zero lower coefficients, the prescribed leading coefficient and a nonzero determinant of the actual moment-series matrix |

The second target uses a nonsingular degree-$b$ matrix moment and
vanishing moments of degrees $b+1,\ldots,d$; the case $b=1$ gives the
coefficient $`(-1)^{d-1}`$ times the moment at order $d$, as in
Lemma 7.3 with $`X=t_i^{-1}`$. It applies over rational-function
coefficient fields in the other parameters, and its determinant
conclusion is derived, not assumed. The identification of the rational
matrix $`H_i(t)`$ with that series, the verification of its
matrix-moment hypotheses and the passage back to a nonzero rational
determinant are paper only. `check_charts.py:univariate_cases` checks
the one-coordinate value $H(2)\neq0$ for $d=2,\ldots,9$.

Proposition 7.1 clears denominators and chooses one finite $t$ with
$Q(t)\neq0$ at `eq:avoidance`. `TR29.finite_chart_avoidance` in
[Avoidance.lean](../lean/TR29/Avoidance.lean) proves that one finite
complex tuple avoids every pole and a finite list of nonzero polynomials
simultaneously. Its premise already requires every input polynomial to
be nonzero; the nonvanishing of the numerators $`N_i`$ comes from
Lemma 7.3 in the paper.

Examples 7.1 to 7.4 display the twenty functions for the cubic triple,
the $`4\times4`$ basic block for $k=2$, the column reversal for
$`d_i=5`$ and the $`20\times20`$ block-diagonal Gram matrix.
`check_charts.py:cubic_chart` builds the twenty evaluation vectors for
one decomposition, up to a common nonzero factor at each node that is
compensated in the weights, and checks block ranks 8, 4, 4, 4, zero
off-diagonal blocks and full rank 20 at $t=(2,3,4)$. Its controls
reject a changed coefficient, a chart with a pole and the chart
$(0,0,0)$, where the additional blocks degenerate.

The proof of Theorem 1.1 at the end of the section combines Lemmas 2.1
and 3.1, Proposition 7.1 and Lemma 6.1 with the cited upper bound. The
list sizes at `eq:Mcount` are the block sizes of
`TR29.tr29_gram_lower_bound`. For $k=1$ the moment form of the lower
bound is also the case $b=1$ of `TR29.univariate_moment_bound`.

## 8. Products of binary monomials

Theorem 8.1 gives, for $k\geq1$ and $`a_i\geq b_i\geq1`$ with
$`d_i=a_i+b_i`$, the rank
$`N(\mathbf a,\mathbf b)=\prod_i(b_i+1)+\sum_i(a_i-b_i)\prod_{j\neq i}(b_j+1)`$.
Its proof combines Proposition 8.1 with Proposition 8.2, and both bounds
are proved in the paper.

Theorem 8.2 is the product-moment lower bound for $`b_i\geq1`$,
$`d_i\geq2b_i`$, moments vanishing in degrees $`b_i+1,\ldots,d_i`$ and
$`\beta_i=m_i(b_i)\neq0`$. For $k=1$ the bound is $`N=d_1-b_1+1`$, and
`TR29.univariate_moment_bound` in
[Univariate.lean](../lean/TR29/Univariate.lean) proves that case; it
needs only $b\leq d$ and permits zero weights and repeated or zero
nodes. For $k\geq2$ the construction of the lists $`\mathscr U`$ and
$`\mathscr V_i`$ and the verification of their Gram properties are
paper only. In the final step at `eq:bm-avoidance`, the paper uses a
common finite parameter and the orthogonal assembly, which are the
statements of `TR29.finite_chart_avoidance` and
`TR29.orthogonal_gram_assembly` under their explicit hypotheses. The
Lean count `TR29.tr29_gram_lower_bound` uses the block sizes of the
case $`b_i=1`$ only; the general count $N$ is not a Lean statement.

- Lemmas 8.1 and 8.2 prove the basic block formula, its determinant and
  the orthogonality of the lists. `check_exact.py:lower` evaluates all
  Gram entries for three rational cubatures with list lengths 33, 54
  and 13, including zero coordinates and a repeated node, checks every
  cross-list entry to vanish and the full Gram determinant to be
  nonzero.
- Lemma 8.3 proves the anti-triangular pattern of each
  $`\mathscr V_i`$ block. `TR29.anti_diagonal_blocks` applies with
  $`r=\delta_i`$ and $`q=q_i`$; `check_exact.py:lower` checks the
  internal zeros for $`s+s'\leq d_i`$.
- Lemma 8.4 is the finite division identity, checked at
  $z=0,1,-2/3$ and $t=5/7$ for every pair $`(d_i,b_i)`$ of the three
  cubatures.
- Lemma 8.5 proves the leading coefficient at `eq:bm-leading` and a
  nonzero $`\det H_i`$. `TR29.matrix_moment_leading` with general $b$
  gives the formal leading coefficient $`(-1)^{d_i-b_i}`$ times the
  degree-$`b_i`$ matrix moment at order $`d_i-b_i+1`$ and a nonzero
  series determinant; the identification with $`H_i(t)`$ is paper only.

Proposition 8.1 reduces an arbitrary decomposition to the moment data
of Theorem 8.2 by an affine chart and differential operators, with
$`\beta_i=\binom{d_i}{b_i}^{-1}`$. It is paper only.

Lemmas 8.6 and 8.7 and Proposition 8.2 give the upper bound: a lattice
of index $N$ whose nonzero vectors avoid the coefficient box at
`eq:bm-box`, character orthogonality, and the $N$-term character
decomposition at `eq:bm-character`. These universal statements are
outside the Lean core. `check_exact.py:upper` checks eight exponent
tuples with $N=54,64,51,20,66,15,8,24$: the lattice determinant and
adjugate, membership at every point of the coefficient box, the
characters of the quotient group, and every coefficient of the identity,
reduced exactly modulo the $N$th cyclotomic polynomial. The tuples
include unequal exponents, balanced factors, four blocks, one block,
two blocks and the cubic W triple.

Remark 8.1 records that Theorem 8.1 with all $`b_i=1`$ contains
Theorem 1.1 and gives an explicit $M$-term decomposition for all
$k\geq1$ and $`d_i\geq2`$, independently of the cited construction.
Example 8.1 gives the ranks 20 and 54; both character identities are
among the checked tuples, and the 54-function Gram list is one of the
checked cubatures. The section also compares the one- and two-block
cases with the cited literature. Remark 8.2 explains why pure-power
factors $`b_i=0`$ are excluded. These remarks are proved or argued in
the paper.

## A. Coordinate factors in the Gram entries

This appendix has no numbered result. It records the coordinate factors
of the products used in Lemma 7.1: the cross factors between
$`\mathcal B_0`$ and $`\mathcal B_i`$ and between $`\mathcal B_i`$ and
$`\mathcal B_j`$, all inside the moment degree box, and the same-family
factors, which are polynomial for $`s+s'\leq d_i`$ and leave one
denominator for $`s+s'=d_i+1`$. These cancellations are paper only;
the zero cross blocks of one decomposition are checked by
`check_charts.py:cubic_chart`.

## B. The leading coefficient of the rational blocks

Lemma B.1 is the finite division identity for $b=1$, written with
$n=d-e$; it is the case $b=1$ of Lemma 8.4. `check_exact.py:lower`
checks it for $d=3$ at the nodes listed above. The detailed proof of
Lemma 7.3 expands $`H_i(t)`$ with this identity and shows at
`eq:det-laurent` that $`\det H_i`$ has a nonzero leading term. The
formal counterpart of that expansion is `TR29.matrix_moment_leading`
with $b=1$; the identification of the rational matrix with the formal
series is paper only.

The seven targets and `TR29.core_theorems` are checked by the Lean
audit's exact-type and axiom probes. The mapping checker verifies that
these references and all 31 numbered results exist and agree with the
map. It does not compile Lean or replace the mathematical checks. See
the [Lean guide](../lean/README.md) and the
[verification guide](../verification/README.md) for their commands.
