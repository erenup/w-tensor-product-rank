# The Exact Partially Symmetric Rank of Products of W-States

Authors: Wenqi Zhu; Ping Nie.

Wenqi Zhu — Mathematical Institute, Woodstock Road, University of Oxford, Oxford, UK, OX2 6GG — wenqi.zhu@maths.ox.ac.uk

Ping Nie — David R. Cheriton School of Computer Science, University of Waterloo — ping.nie@uwaterloo.ca

Read the [paper](paper/main.pdf) and its [LaTeX source](paper/main.tex).
The theorem answers the [catalogue question](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/eb7c9d64f91757a82fbe9167e80ab9c1b7f36c22/tensor-computations/TR-29/README.md)
for every number of factors and all degrees in its range.

## Main theorem

For every integer $k\geq2$ and all integers $`d_i\geq3`$, over the complex
numbers,

```math
R_{(d_1,\ldots,d_k)}\!\left(\prod_{i=1}^k x_i^{d_i-1}y_i\right)
=2^{k-1}\left(\sum_{i=1}^k d_i-2k+2\right)=M.
```

The pair $`(x_i,y_i)`$ represents the $i$th symmetric block, of order
$`d_i`$, so the polynomial represents the product
$`W_{d_1}\otimes\cdots\otimes W_{d_k}`$ of generalized W-states up to a
nonzero scalar. The partially symmetric rank is the least $r$ in

```math
\prod_{i=1}^k x_i^{d_i-1}y_i
=\sum_{\ell=1}^r c_\ell\prod_{i=1}^k
(a_{i\ell}x_i+b_{i\ell}y_i)^{d_i},
\qquad c_\ell,a_{i\ell},b_{i\ell}\in\mathbb C,
```

with the blocks and their degrees fixed. This is Theorem 1.1 of the
paper. The upper bound is
[Theorem 1.1](https://arxiv.org/abs/2512.05828v1) of Canino, Casarotti
and Santarsiero; Section 8 of the paper gives an independent explicit
$M$-term decomposition. The lower bound applies to every complex
decomposition, without any restriction on its support, and allows
repeated points and zero coordinates. In particular, the cubic triple
$`x_1^2y_1x_2^2y_2x_3^2y_3`$ has rank **20**, and the $k$-fold cubic
product has rank $`2^{k-1}(k+2)`$.

An invertible change of coordinates turns any decomposition into $r$
weighted points $`z_\ell\in\mathbb C^k`$ with nonzero complex weights.
Matching every coefficient gives product moment conditions on the full
box $`0\leq e_i\leq d_i`$. Explicit rational test functions, one basic
family of $`2^k`$ functions and one additional family of
$`(d_i-2)2^{k-1}`$ functions per block, give an evaluation matrix $E$
with $r$ rows and $M$ columns, and their weighted bilinear Gram matrix

```math
\mathcal G=E^{\mathsf T}WE
```

is block diagonal. The basic block is a Kronecker product with nonzero
determinant. Each additional block becomes block triangular after its
block columns are reversed, with diagonal blocks $`H_i(t)`$, and an
exact Laurent expansion shows that each
$`\det H_i`$ is a nonzero rational function of the auxiliary parameters
$t$. One finite parameter vector avoids every pole and every zero of
these determinants simultaneously; there $`\mathcal G`$ is invertible,
so the $M$ columns of $E$ are independent and $r\geq M$. The pairing
uses transpose, with complex weights and no positivity assumption.

The rank refers to the prescribed partially symmetric blocks. The
theorem makes no claim about border rank, ordinary tensor rank or rank
after grouping modes from different blocks.

## Products of binary monomials

For every integer $k\geq1$ and integers $`a_i\geq b_i\geq1`$, set
$`d_i=a_i+b_i`$. With these $k$ symmetric blocks fixed,

```math
R_{(d_1,\ldots,d_k)}\!\left(\prod_{i=1}^k x_i^{a_i}y_i^{b_i}\right)
=\prod_{i=1}^k(b_i+1)
 +\sum_{i=1}^k(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

Empty products equal one. This is Theorem 8.1 of the paper. The lower
bound comes from a product-moment theorem (Theorem 8.2) for weighted
points whose coordinate moments vanish above degree $`b_i`$ and are
nonzero in degree $`b_i`$, together with a reduction of every
decomposition to such moments (Proposition 8.1). The upper bound is an
explicit decomposition (Proposition 8.2) indexed by the characters of
$`\mathbb Z^k/\Delta\mathbb Z^k`$. Here
$`\Delta=\mathrm{diag}(b_1+1,\ldots,b_k+1)+\delta\mathbf 1^{\mathsf T}`$
with $`\delta_i=a_i-b_i`$; its columns generate a lattice whose index
equals the rank and whose only point in the box
$`\prod_i[-a_i,b_i]`$ of exponent differences is zero. Both bounds are proved in the
paper. The triple product of $`x^3y^2`$ has rank **54**.

The case $`b_i=1`$ is the W-state formula, now for all $k\geq1$ and
$`d_i\geq2`$ (Remark 8.1). The one- and two-block cases overlap with
earlier work discussed in Section 8 of the paper: the classical rank of
a binary monomial, a two-block upper bound of Gałązka, a two-block lower
bound of Ballico, Bernardi, Gesmundo, Oneto and Ventura, and the exact
two-block formula in an unpublished manuscript of Behr. Pure-power factors $`b_i=0`$ are excluded
(Remark 8.2). The theorem makes no claim about real, border, cactus,
unrestricted nonsymmetric or regrouped-mode rank.

## Evidence status

- **Formally proved in Lean:** seven universal algebraic targets,
  combined in `TR29.core_theorems : TR29.CoreTheorems`: the
  one-coordinate moment lower bound, a geometric-series inverse, the
  matrix-moment leading coefficient and nonzero series determinant,
  anti-diagonal block nonsingularity, orthogonal bilinear Gram
  independence, the W-product count under explicit Gram hypotheses, and
  one finite chart avoiding specified poles and nonzero polynomials. The
  permitted axioms are exactly `propext`, `Classical.choice` and
  `Quot.sound`. The one-coordinate bound is the case $k=1$ of
  Theorem 8.2, and the one-block case of the Gram statement is the
  implication of Lemma 6.1; no rank formula is a Lean theorem. The [formal scope](lean/SCOPE.md) states
  the exact hypotheses and conclusions.
- **Exact computation:** standard-library integer, rational and
  cyclotomic checks verify all coefficients and moments of one 20-term
  decomposition of the cubic triple and a nonsingular $`20\times20`$
  Gram matrix for it, one-coordinate moment and block checks in
  degrees 2 to 9,
  every coefficient of eight character decompositions including the
  54-term example, and three full Gram calculations with zero
  coordinates and a repeated point. Required rejections of corrupted
  inputs are part of each run. These are finite supporting checks.
- **Proved in the paper only:** the reduction of an arbitrary
  decomposition to moments (Lemmas 2.1, 3.1 and 4.1 and
  Proposition 8.1); the specific test functions and their cross-block
  cancellations (Lemmas 7.1 and 8.2, Appendix A); the identification of
  each rational block $`H_i`$ with its formal series and its nonzero
  determinant numerator (Lemmas 7.3 and 8.5, Appendix B); the
  multivariate product-moment theorem for $k\geq2$; the lattice and
  character construction for all exponents; and both rank formulas. The
  W upper bound is also available in the cited construction. The
  [section map](paper-lean-mapping/by-section.md) gives the evidence for
  each numbered result.
- **Review:** the [review record](verification/reviews/README.md) contains
  the independent informal AI-agent audits of the paper's mathematics (two
  referees for Sections 1–7, a check of the applied corrections, and two
  referees for Section 8), all accepting with corrections that are
  incorporated. Wenqi Zhu checked the complete argument, and Haibin Chen
  (Qufu Normal University), a specialist in tensor decompositions who was
  not involved in the work, reviewed the proof and found it correct.
- **Open:** the paper does not determine real, border, cactus,
  unrestricted nonsymmetric or regrouped-mode ranks of these products,
  or ranks of products that contain pure-power factors. A formal proof
  of the complete moment-to-rank argument is outside the Lean core.

## Where to read

Start with the [guide from moments to the rank bound](paper-lean-mapping/README.md),
then the [paper](paper/main.pdf). Section 1 states Theorem 1.1;
Sections 2 to 4 turn a decomposition into weighted points and moment
conditions; Sections 5 and 6 build the weighted Gram matrix and derive
the dimension bound; Section 7 constructs the test functions, proves
block nondegeneracy and completes the proof. Section 8 proves the
binary-monomial theorem with its lower bound, reduction and character
decomposition. Appendices A and B give the Gram-entry factors and the
Laurent coefficient. The [section-by-section map](paper-lean-mapping/by-section.md)
lists every numbered result with its Lean declarations, exact checks or
paper-only status.

Plain-text versions are the [W-product statement](verification/core/proofs/STATEMENT.md)
and [proof](verification/core/proofs/PROOF.md), and the
[binary-monomial statement](verification/core/families/monomial-products/proofs/STATEMENT.md),
[proof](verification/core/families/monomial-products/proofs/PROOF.md) and
[literature discussion](verification/core/families/monomial-products/proofs/LITERATURE.md).
For the formal core, read [Definitions](lean/TR29/Definitions.lean),
[Statement](lean/TR29/Statement.lean), then [Proofs](lean/TR29/Proofs.lean).
The [Lean guide](lean/README.md), the [exact-check guide](verification/README.md)
and the [verification record](VERIFICATION.md) give reproduction details.

## Reproduce the checks

From the repository root, with Python 3.11 or later:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
python3 -S -s -B paper-lean-mapping/build_and_check.py
python3 -S -s -B -O paper-lean-mapping/build_and_check.py
python3 tools/check_markdown_math.py
sha256sum --check SHA256SUMS
(cd paper && sha256sum --check SHA256SUMS)
```

The Python programs use only the standard library, and their normal and
optimized outputs must agree. The entry point also runs the
binary-monomial suite. With the pinned Lean toolchain installed, fetch
the pinned dependency cache from `lean/` and run the verifier from the
repository root:

```sh
(cd lean && lake exe cache get)
python3 -B lean/verify
```

See [VERIFICATION.md](VERIFICATION.md) for the observed outputs and
[paper/README.md](paper/README.md) for the manuscript build.

## Layout

- `paper/`: LaTeX source with eight section files and two appendices, bibliography, PDF, build guide, licence and source manifest.
- `lean/`: the pinned Lean project for the seven algebraic targets, with its audit and verifier.
- `paper-lean-mapping/`: reading guide, result map, machine-readable mapping and its checker.
- `verification/`: one entry point for the exact checks; `core/proofs/` holds the plain-text W-product statement and proof, `core/verification/` the exact W checks, and `core/families/monomial-products/` the plain-text statement, proof, literature discussion and exact checks for products of binary monomials.
- `tools/`: a static guard for GitHub Markdown math.

## License and citation

Files outside `paper/` are available under the [MIT license](LICENSE).
The files in `paper/`, including the manuscript source and PDF, are licensed
under [CC BY-SA 4.0](paper/LICENSE).
Citation information is in [CITATION.cff](CITATION.cff).

## Acknowledgements

We thank [NetMind.AI](https://www.netmind.ai/) and [AI4ALPHA](https://www.ai4alpha.ca/) for their
support of this project. The research of Wenqi Zhu was also supported by the Engineering and Physical Sciences Research
Council under grant EP/Y028872/1, *Mathematical Foundations of Intelligence: An "Erlangen Programme" for AI*.
