# The partially symmetric rank of products of binary monomials

Read the [paper](main.pdf) or its [LaTeX source](main.tex).
Authors: TBD. Acknowledgements: TBD.

The introduction starts from the known W-product upper bound and asks
why every decomposition needs at least that many terms. Normalized
coordinates give moment conditions, explicit test functions give a
weighted bilinear Gram matrix, and its invertibility gives the lower
count. The proof includes block nondegeneracy and one simultaneous
finite parameter choice, allowing repeated nodes and zero coordinates.

For every $k\geq2$ and $d_i\geq3$, over the complex numbers,

```math
R_{(d_1,\ldots,d_k)}(W_{d_1}\otimes\cdots\otimes W_{d_k})
=2^{k-1}\left(\sum_i d_i-2k+2\right).
```

More generally, for every $k\geq1$ and integers $a_i\geq b_i\geq1$,
with the symmetric blocks of degrees $a_i+b_i$ fixed,

```math
R\!\left(\prod_i x_i^{a_i}y_i^{b_i}\right)
=\prod_i(b_i+1)+\sum_i(a_i-b_i)\prod_{j\ne i}(b_j+1).
```

Empty products equal one. The paper supplies the full product-moment
lower bound and the matching finite-character construction. It includes
the known one- and two-block overlaps and the balanced-exponent endpoint.
Pure-power factors with $b_i=0$ are excluded. Real, border, cactus,
unrestricted nonsymmetric and regrouped-mode ranks are outside the
statements. SOS decompositions are discussed only as related background
with different admissible terms.

## Build

From this directory, with the packages listed in `main.tex` and `latexmk`:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The source reads the three files in `sections/` and the inline
`bibliography.tex`; no BibTeX step is needed. The output is `build/main.pdf`;
the included PDF is [main.pdf](main.pdf). Build files are ignored.

## Evidence and scope

The [result map](../paper-lean-mapping/by-section.md) connects numbered
paper results to the seven [Lean algebraic targets](../lean/SCOPE.md),
finite exact checks, and the portions proved only in writing. The Lean
core does not state either complete rank formula. In particular, the
specific multivariate Gram construction, rational-to-series and numerator
identifications, tensor reduction and character upper bound remain
outside its contract.

The [W-product proof](../proofs/PROOF.md) and
[binary-monomial proof](../families/monomial-products/proofs/PROOF.md)
state the mathematical arguments in plain text. From this directory,
run both exact supporting suites through their single entry point:

```sh
python3 -S -s -B ../verification/run.py
python3 -S -s -B -O ../verification/run.py
```

Their guides describe finite ranges, output bindings and required
rejections. Finite examples do not replace the universal proof.
Reproduction commands and recorded results are in [VERIFICATION.md](../VERIFICATION.md).

## License

The manuscript license is TBD; see [LICENSE](LICENSE).
