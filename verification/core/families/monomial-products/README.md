# Exact rank of products of positive binary monomials

For every integer `k≥1` and all integers `a_i≥b_i≥1`, over the complex
numbers, the partially symmetric rank with blocks of degrees `a_i+b_i`
fixed is

```math
R\!\left(\prod_{i=1}^{k}x_i^{a_i}y_i^{b_i}\right)
 =\prod_{i=1}^{k}(b_i+1)
  +\sum_{i=1}^{k}(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

Decompositions may use arbitrary complex coefficients and factor vectors.
There is no support, reality or genericity restriction. Empty products
equal one. In particular, the triple product of `x³y²` has rank **54**.
The [statement](proofs/STATEMENT.md) gives the full quantifiers and the
[proof](proofs/PROOF.md) proves both bounds without an external theorem:
the lower bound uses product-moment Gram matrices, and the upper bound
uses a finite lattice quotient and its characters.

The abstract lower theorem allows `b_i≥1`, `d_i≥2b_i`, arbitrary lower
moments, zero moments above degree `b_i`, and a nonzero moment of degree
`b_i`. For any weighted finite node set matching these product moments
through degree `d_i` in each coordinate, it gives

```math
n\ge\prod_i(b_i+1)
       +\sum_i(d_i-2b_i)\prod_{j\ne i}(b_j+1).
```

Nodes may repeat, any coordinate may be zero, and weights may be arbitrary
nonzero complex numbers.

The target subfamily is `k≥3` with at least one `b_i≥2`. The full theorem
also contains the known one- and two-block cases and the all-`b_i=1`
[W-product formula](../../proofs/STATEMENT.md); those overlaps are not
claimed as independent new results. The [literature comparison](proofs/LITERATURE.md)
is limited to the inspected sources and makes no exhaustive novelty or
priority claim. The original W-product proof uses the cited
Canino–Casarotti–Santarsiero upper theorem; this extension includes its own
elementary upper construction.

Pure-power factors `b_i=0` are excluded: the displayed formula would already
fail for `x^a`. The result concerns finite complex rank with fixed symmetric
blocks. It makes no assertion about real, unrestricted nonsymmetric,
grouped-mode, cactus or border rank.

The [exact checks](verification/README.md) support the arithmetic and
construction in finite cases. They do not replace the proof for all
parameters.
