# The Exact Partially Symmetric Rank of Products of W-States

Authors: Wenqi Zhu; Ping Nie.

Wenqi Zhu — Mathematical Institute, Woodstock Road, University of Oxford, Oxford, UK, OX2 6GG — wenqi.zhu@maths.ox.ac.uk

Ping Nie — David R. Cheriton School of Computer Science, University of Waterloo — ping.nie@uwaterloo.ca

The [paper](main.pdf) proves that, for every $k\geq2$ and all
$`d_i\geq3`$, the partially symmetric rank over the complex numbers of
$`\prod_{i=1}^k x_i^{d_i-1}y_i`$, with the $k$ symmetric blocks fixed, is

```math
R_{(d_1,\ldots,d_k)}\Bigl(\prod_{i=1}^k x_i^{d_i-1}y_i\Bigr)
=2^{k-1}\Bigl(\sum_{i=1}^k d_i-2k+2\Bigr).
```

The lower bound (Sections 2 to 7) applies to every decomposition and
uses moment conditions and a weighted bilinear Gram matrix; the upper
bound is the construction of Canino, Casarotti and Santarsiero.
Section 8 determines, for every $k\geq1$ and all integers
$`a_i\geq b_i\geq1`$, the rank of $`\prod_i x_i^{a_i}y_i^{b_i}`$ with
blocks of degrees $`a_i+b_i`$:

```math
\prod_{i=1}^k(b_i+1)+\sum_{i=1}^k(a_i-b_i)\prod_{j\ne i}(b_j+1),
```

with a matching explicit finite-character decomposition. Appendices A
and B record the Gram-entry factors and the leading Laurent coefficient.

The source is [main.tex](main.tex), with the eight section files in
[sections/](sections/), the two appendix files in
[appendices/](appendices/) and the bibliography [refs.bib](refs.bib).
Build from this directory with LaTeX, BibTeX and `latexmk`:

```sh
sha256sum -c SHA256SUMS
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

The rebuilt PDF is `build/main.pdf`; it has 16 pages, and its extracted
text is identical to that of the included [main.pdf](main.pdf). Standard
TeX Live packages suffice. The source and PDF list the authors above;
Wenqi Zhu is the corresponding author. [SHA256SUMS](SHA256SUMS) lists
every file in this directory except itself and the generated `build/`
directory.

The [result map](../paper-lean-mapping/by-section.md) gives the evidence
for every numbered result, and the [verification record](../VERIFICATION.md)
gives the reproduction commands.

All files in this directory, including the manuscript source and PDF, are
licensed under [CC BY-SA 4.0](LICENSE).
