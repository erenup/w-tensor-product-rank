# The partially symmetric rank of products of binary monomials

Authors: TBD

Repository: [erenup/w-tensor-product-rank](https://github.com/erenup/w-tensor-product-rank).

Read the [paper](paper/main.pdf) and its [LaTeX source](paper/main.tex).
The [catalogue question](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/eb7c9d64f91757a82fbe9167e80ab9c1b7f36c22/tensor-computations/TR-29/README.md)
asks for the partially symmetric rank of products of generalized W tensors.
The symmetric blocks stay fixed throughout.

## From the known upper bound to the exact rank

For every integer $k\geq2$ and all integers $d_i\geq3$, over the complex
numbers,

```math
R_{(d_1,\ldots,d_k)}(W_{d_1}\otimes\cdots\otimes W_{d_k})
=2^{k-1}\left(\sum_{i=1}^k d_i-2k+2\right)=M.
```

Here $W_d$ is represented, up to a nonzero scalar, by $x^{d-1}y$.
The rank counts the least number of terms in

```math
\prod_{i=1}^k x_i^{d_i-1}y_i
=\sum_{\ell=1}^r c_\ell\prod_{i=1}^k
(a_{i\ell}x_i+b_{i\ell}y_i)^{d_i},
\qquad c_\ell,a_{i\ell},b_{i\ell}\in\mathbb C.
```

Canino–Casarotti–Santarsiero's [Theorem 1.1](https://arxiv.org/abs/2512.05828v1)
constructs an upper bound of $M$ terms. The lower bound applies to every
complex decomposition, allowing repeated nodes and zero coordinates.
In particular, the cubic triple has rank **20**, and the $k$-fold cubic
product has rank $2^{k-1}(k+2)$.

An invertible change of coordinates normalizes any proposed decomposition
into weighted affine points. Matching every coefficient gives moment
conditions on the full coordinate-degree box. Linearity extends these
conditions to that polynomial space. Explicit test functions, in one
basic batch and one additional batch per block, give an evaluation
matrix $E$ with $r$ rows and $M$ columns. Their weighted bilinear Gram
matrix is

```math
G=E^{\mathsf T}WE.
```

The proof makes $G$ invertible at one finite choice of auxiliary parameters;
the $M$ columns of $E$ must then be independent, so $r\geq M$. The essential
step is block nondegeneracy: exact Laurent coefficients show that the
relevant determinants are nonzero rational functions, and a finite
polynomial avoidance argument chooses all parameters simultaneously.
The pairing uses transpose, with complex weights and no positivity
assumption. The [reading guide](paper-lean-mapping/README.md) explains
this chain and distinguishes polynomial moments from rational evaluations.

## The full binary-monomial theorem

For every integer $k\geq1$ and integers $a_i\geq b_i\geq1$, set
$d_i=a_i+b_i$. With these $k$ symmetric blocks fixed,

```math
R_{(d_1,\ldots,d_k)}\!\left(\prod_{i=1}^k x_i^{a_i}y_i^{b_i}\right)
=\prod_{i=1}^k(b_i+1)
 +\sum_{i=1}^k(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

Empty products equal one. The lower bound uses the general product-moment
argument; an explicit finite-character construction supplies a matching
decomposition. Both bounds for this theorem are proved in the paper.
The triple product of $x^3y^2$ has rank **54**. The theorem includes balanced
exponents and the known one- and two-block cases. Those overlaps, and the
W specialization, are recorded in the [literature discussion](families/monomial-products/proofs/LITERATURE.md).

These are exact complex ranks for the prescribed blocks. Pure-power
factors $b_i=0$ are excluded. The theorems make no claim about real,
border, cactus, unrestricted nonsymmetric, or regrouped-mode rank.
SOS tensor decompositions use squares of real homogeneous polynomials,
which are different admissible terms; their ranks are not identified
with the ranks here. The paper cites that subject only as background.

## Evidence status

- **Formally proved in Lean 4 with Mathlib:** seven universal algebraic
  targets, combined in `TR29.core_theorems`: the univariate moment lower
  bound; a geometric-series inverse; the matrix-moment leading coefficient
  and nonzero series determinant; anti-diagonal block nonsingularity;
  orthogonal bilinear Gram independence; the W-product count under explicit
  Gram hypotheses; and one finite chart avoiding specified poles and
  nonzero polynomials. The only permitted axioms are `propext`,
  `Classical.choice` and `Quot.sound`. The [formal scope](lean/SCOPE.md)
  states the exact hypotheses and conclusions.
- **Exact computation:** standard-library integer, rational and cyclotomic
  checks verify selected coefficient, moment, Gram and character identities,
  including the 20- and 54-term examples, zero and repeated nodes, and
  corrupted inputs that must fail. These are finite supporting checks.
- **Proved in the paper only:** the full multivariate product-moment
  theorem; the specific test functions and their cross-block cancellation;
  identification of each rational block, its series and determinant
  numerator; reduction of arbitrary decompositions to moments; the general
  binary-monomial count, lattice argument and finite-character construction;
  and the full exact rank formulas. The W upper bound is also available in
  the cited construction. The Lean Gram count has additional Gram
  hypotheses and is not the full moment-to-rank implication.

## Where to read

Start with the [reading guide](paper-lean-mapping/README.md), then the
[paper](paper/main.pdf). Its introduction leads from the known W upper
bound to moments, a weighted Gram matrix, and the lower count. The
remaining sections give the complete general lower bound, the reduction
from decompositions, and the matching character construction.

The [section-by-section map](paper-lean-mapping/by-section.md) records each
numbered result and its evidence. The [W-product statement and proof](proofs/STATEMENT.md)
and [binary-monomial statement and proof](families/monomial-products/proofs/STATEMENT.md)
provide plain-text versions. The [verification record](VERIFICATION.md)
gives commands and the precise scope of each check.

## Reproduce the checks

Use Python 3.11 or later for the standard-library checks:

```sh
python3 -S -s -B verification/run.py
python3 -S -s -B -O verification/run.py
python3 -I -B paper-lean-mapping/build_and_check.py
python3 -I -B -O paper-lean-mapping/build_and_check.py
python3 -I -B tools/check_markdown_math.py
python3 -I -B -O tools/check_markdown_math.py
```

For the seven formal targets, install the pinned Lean toolchain, fetch
the pinned Mathlib cache, and run the [Lean verifier](lean/README.md):

```sh
cd lean
lake exe cache get
./verify
```

The [paper guide](paper/README.md) gives the LaTeX build command.

## Layout

- `paper/`: manuscript, bibliography, built PDF and license notice.
- `proofs/`: W-product statement and complete lower-bound proof.
- `families/monomial-products/`: general statement, proof, literature and exact checks.
- `lean/`: the seven algebraic targets, pinned dependencies and verifier.
- `paper-lean-mapping/`: reading guide, result map and correspondence checker.
- `verification/`: one entry point for both exact supporting suites.
- `tools/`: the static Markdown math guard.

## License and citation

Files outside `paper/` are available under the [MIT license](LICENSE).
The [paper license](paper/LICENSE) is TBD. Author information is TBD in
[CITATION.cff](CITATION.cff).

## Acknowledgements

TBD.
